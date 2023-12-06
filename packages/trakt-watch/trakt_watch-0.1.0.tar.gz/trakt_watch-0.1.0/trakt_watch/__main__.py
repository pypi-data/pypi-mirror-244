#!/usr/bin/env python3

import json
from typing import (
    get_args,
    Literal,
    Optional,
    NamedTuple,
    Union,
    Iterator,
    Iterable,
    Any,
)
from datetime import datetime, timezone

import click
from logzero import logger  # type: ignore[import]
from traktexport.export import _check_config

from trakt.movies import Movie  # type: ignore[import]
from trakt.tv import TVShow, TVEpisode  # type: ignore[import]
from trakt.people import Person  # type: ignore[import]
from trakt.sync import search  # type: ignore[import]

_check_config()

USERNAME: Optional[str] = None


@click.group()
@click.option(
    "-u",
    "--username",
    help="Trakt username",
    required=True,
    envvar="TRAKT_USERNAME",
    show_envvar=True,
)
def main(username: str) -> None:
    global USERNAME

    USERNAME = username


class MovieId(NamedTuple):
    id: str

    def trakt(self) -> Movie:
        from trakt.movies import Movie

        mv = Movie(self.id, year=None, slug=self.id)
        mv._get()
        return mv


class EpisodeId(NamedTuple):
    id: str
    season: int
    episode: int

    def trakt(self) -> TVEpisode:
        from trakt.tv import TVEpisode

        ep = TVEpisode(show=self.id, season=self.season, number=self.episode)
        ep._get()
        return ep


class TVShowId(NamedTuple):
    id: str

    def trakt(self) -> TVShow:
        from trakt.tv import TVShow

        tv = TVShow(self.id)
        tv._get()
        return tv


Input = Union[MovieId, EpisodeId, TVShowId]


def _print_response_pretty(d: Any, rating: bool = False) -> bool:
    if not isinstance(d, dict):
        return False
    try:
        if "added" in d or "deleted" in d:
            key = "added" if "added" in d else "deleted"
            if d[key]["movies"] or d[key]["episodes"]:
                print_text = "Added" if key == "added" else "Removed"
                if rating:
                    print_text += " rating"
                click.secho(f"{print_text}:", bold=True, fg="green")
                if d[key]["movies"]:
                    click.echo(f"Movies: {d[key]['movies']}")
                if d[key]["episodes"]:
                    click.echo(f"Episodes: {d[key]['episodes']}")
        else:
            return False

        not_found_lines = []
        for k, v in d["not_found"].items():
            # return false so whole error gets printed
            if not isinstance(v, list):
                return False
            for item in v:
                not_found_lines.append(f"{k}: {repr(item)}")

        if not_found_lines:
            click.secho("Not found:", bold=True, fg="red", err=True)
            for line in not_found_lines:
                click.echo(line)

        click.echo()
        return True
    except Exception:
        # if failed to access any of the keys, skip nice print
        return False


def _print_response(d: Any, rating: bool = False) -> None:
    if _print_response_pretty(d, rating=rating):
        return
    if isinstance(d, dict):
        click.echo(json.dumps(d, indent=2), err=True)
    else:
        click.echo(d, err=True)


def _parse_url_to_input(url: str) -> Input:
    from urllib.parse import urlsplit

    parts = urlsplit(url)
    if parts.netloc != "trakt.tv":
        click.secho(
            f"Warning; Invalid URL netloc: {parts.netloc}, expected trakt.tv",
            fg="yellow",
            err=True,
        )

    prts = [u.strip() for u in parts.path.split("/") if u.strip()]

    match prts:
        case ["movies", id, *_]:
            return MovieId(id)
        case ["shows", id, "seasons", season, "episodes", episode, *_]:
            return EpisodeId(id, int(season), int(episode))
        case ["shows", id, *_]:
            return TVShowId(id)
        case _:
            raise ValueError(f"Invalid URL parts: {prts}")


def _mark_watched(
    input: Input,
    *,
    watched_at: Union[datetime, None, Literal["released"]] = None,
    rating: Optional[int] = None,
) -> None:
    if isinstance(input, MovieId):
        mv = input.trakt()
        _print_response(mv.mark_as_seen(watched_at=watched_at))
        if rating is not None or click.confirm("Set rating?", default=True):
            if not rating:
                rating = click.prompt("Rating", type=int)
            assert isinstance(rating, int)
            _print_response(mv.rate(rating), rating=True)
    elif isinstance(input, EpisodeId):
        ep = input.trakt()
        _print_response(ep.mark_as_seen(watched_at=watched_at))
    elif isinstance(input, TVShowId):
        # prompt user if they want to watch an entire show or just an episode
        if click.confirm("Really mark entire show as watched?", default=False):
            _print_response(input.trakt().mark_as_seen(watched_at=watched_at))
    else:
        raise ValueError(f"Invalid input type: {type(input)}")


def _parse_datetime(
    ctx: click.Context, param: click.Argument, value: Optional[str]
) -> Union[datetime, None, Literal["released"]]:
    import dateparser
    import warnings

    # remove pytz warning from dateparser module
    warnings.filterwarnings("ignore", "The localize method is no longer necessary")

    if value is None:
        return None

    ds = value.strip()
    if ds == "released":
        return "released"
    dt = dateparser.parse(ds)
    if dt is None:
        raise click.BadParameter(f"Could not parse '{ds}' into a date")
    else:
        ts = dt.timestamp()
        local_dt = datetime.fromtimestamp(ts)
        click.echo(f"Date: {local_dt}", err=True)
        return datetime.fromtimestamp(ts, tz=timezone.utc)


def _display_search_entry(entry: Any, *, include_slug: bool = False) -> str:
    buf: str = ""
    if isinstance(entry, Movie):
        buf += f"Movie:\t{entry.title} ({entry.year})"
    elif isinstance(entry, TVEpisode):
        buf += f"Episode:\t{entry.show} S{entry.season}E{entry.episode} - {entry.title}"
    elif isinstance(entry, TVShow):
        buf += f"Show:\t{entry.title} ({entry.year})"
    elif isinstance(entry, Person):
        buf += f"Person:\t{entry.name}"
    else:
        raise ValueError(f"Invalid entry type: {type(entry)}")

    if include_slug:
        buf += f" | {entry.ext}"

    return buf


def _handle_pick_result(
    user_input: str,
) -> Optional[int]:
    if user_input.strip() in {"n", "q"}:
        raise click.Abort()
    try:
        choice = int(user_input)
        return choice
    except ValueError:
        click.secho(f"Could not parse '{user_input}' into a number", fg="red", err=True)
        return None


allowed = ["M", "S", "I", "E", "A", "U"]


def _search_trakt() -> Input:
    # prompt user to ask if they want to search for a
    # particular type of media, else just search for all
    # types
    click.echo(
        "[M]ovie\n[S]how\n[E]pisode name\nEp[I]sode - Show w/ Season/Episode num\n[U]rl\n[A]ll\nWhat type of media do you want to search for? ",
        nl=False,
    )
    pressed = click.getchar().upper()
    click.echo()
    if pressed not in allowed:
        click.secho(
            f"Invalid choice: {pressed}, should be one of ({', '.join(allowed)})",
            fg="red",
            err=True,
        )
    if pressed == "U":
        urlp = click.prompt("Url", type=str)
        return _parse_url_to_input(urlp)
    # 'movie', 'show', 'episode', or 'person'
    pressed = pressed if pressed in allowed else "A"
    media_type: Optional[str] = {
        "M": "movie",
        "S": "show",
        "I": "show",
        "E": "episode",
        "A": None,
    }.get(pressed)

    search_term = click.prompt(f"Search for {media_type or 'all'}", type=str)
    results = search(search_term, search_type=media_type)  # type: ignore[arg-type]

    if not results:
        raise click.ClickException("No results found")

    choice: Optional[int] = None

    while choice is None:
        click.echo("Results:")
        for i, result in enumerate(results, 1):
            click.echo(f"{i}: {_display_search_entry(result, include_slug=True)}")

        choice = click.prompt(
            f"Pick result - enter 1-{len(results)}, or q to quit",
            default="1",
            value_proc=_handle_pick_result,
        )
        if choice is None:
            continue
        assert isinstance(choice, int), f"Invalid choice type: {choice} {type(choice)}"
        if choice < 1 or choice > len(results):
            click.secho(f"Invalid choice, must be 1-{len(results)}", fg="red", err=True)
            choice = None

    result = results[choice - 1]
    result._get()
    inp = _parse_url_to_input(f"https://trakt.tv/{result.ext}")
    if pressed == "I":
        season = click.prompt("Season", type=int)
        episode = click.prompt("Episode", type=int)
        inp = EpisodeId(inp.id, season, episode)
    return inp


def _handle_input(
    ctx: click.Context, param: click.Argument, url: Optional[str]
) -> Input:
    if url is not None:
        return _parse_url_to_input(url)
    else:
        return _search_trakt()


@main.command(short_help="mark movie/episode as watched")
@click.option(
    "--url",
    "inp",
    help="URL to watch",
    required=False,
    default=None,
    type=click.UNPROCESSED,
    callback=_handle_input,
)
@click.option(
    "-a",
    "--at",
    help="Watched at time (date like string, or 'released')",
    callback=_parse_datetime,
    default=None,
)
@click.option(
    "-r",
    "--rating",
    help="Rating",
    type=click.IntRange(min=1, max=10),
    default=None,
)
def watch(
    inp: Input, at: Union[datetime, Literal["released"], None], rating: Optional[int]
) -> None:
    """
    Pass the movie/episode url to mark it as watched right now
    """
    _mark_watched(inp, watched_at=at, rating=rating)
    _print_recent_history(_recent_history_entries(limit=10))


from traktexport.dal import _parse_history, HistoryEntry

HistoryType = Literal["movies", "episodes"]


def _recent_history_entries(
    *, limit: int = 10, page: int = 1, history_type: Optional[HistoryType] = None
) -> Iterator[HistoryEntry]:
    from traktexport.export import _trakt_request

    username = USERNAME
    assert username is not None

    url_parts = ["users", username, "history"]
    if history_type is not None:
        url_parts.append(history_type)

    data = _trakt_request(
        f"{'/'.join(url_parts)}?page={page}&limit={limit}", logger=None, sleep_time=0
    )

    yield from _parse_history(data)


def _display_history_entry(entry: HistoryEntry, include_id: bool = False) -> str:
    from traktexport.dal import Movie, Episode

    watched_at = entry.watched_at.astimezone().strftime("%Y-%m-%d %H:%M:%S")
    buf: str
    if isinstance(entry.media_data, Movie):
        buf = f"{watched_at} {entry.media_data.title}"
    elif isinstance(entry.media_data, Episode):
        ep = entry.media_data
        assert isinstance(ep, Episode)
        buf = f"{watched_at} {ep.show.title} S{ep.season}E{ep.episode} - {ep.title}"
    else:
        raise ValueError(f"Invalid media_type: {entry.media_type}")

    if include_id:
        buf += f" ({entry.history_id})"
    return buf


def _print_recent_history(
    history: Iterable[HistoryEntry], include_id: bool = False
) -> None:
    history = list(history)  # consume so the request happens
    click.secho("Recent history:", bold=True)
    for i, entry in enumerate(history, 1):
        click.echo(f"{i}: {_display_history_entry(entry, include_id=include_id)}")


@main.command(short_help="remove recent watched item")
@click.option("-i/-a", "--interactive/--non-interactive", default=True, is_flag=True)
@click.option("--yes", "-y", is_flag=True, default=False, help="Skip confirmation")
@click.argument("limit", type=int, default=10)
def unwatch(interactive: bool, yes: bool, limit: int) -> None:
    """
    Remove the last watched item from your history
    """
    from traktexport.export import _trakt_request

    data = list(_recent_history_entries(limit=limit))
    picked: HistoryEntry = data[0]
    if interactive:
        picked_int: Optional[int] = None
        _print_recent_history(data, include_id=True)
        while picked_int is None:
            picked_int = click.prompt(
                "Pick item to remove, q to quit",
                default="1",
                value_proc=_handle_pick_result,
            )
            if picked_int is None:
                continue
            if picked_int < 1 or picked_int > len(data):
                picked_int = None
                click.secho(
                    f"Invalid choice, must be 1-{len(data)}", fg="red", err=True
                )

        picked = data[picked_int - 1]

    click.echo(f"Removing {_display_history_entry(picked, include_id=True)}...")

    last_history_id = picked.history_id
    if not yes:
        click.confirm("Remove from history?", abort=True, default=True)

    click.echo(f"Removing {last_history_id}...")

    resp = _trakt_request(
        "sync/history/remove",
        method="post",
        data={"movies": [], "episodes": [], "ids": [last_history_id]},
        logger=logger,
        sleep_time=0,
    )

    _print_response(resp)
    _print_recent_history(_recent_history_entries(limit=limit), include_id=True)


@main.command(short_help="show recent history")
@click.option(
    "-t",
    "--type",
    "history_type",
    type=click.Choice(list(get_args(HistoryType)), case_sensitive=False),
)
@click.argument("limit", type=int, default=10)
def recent(limit: int, history_type: Optional[HistoryType]) -> None:
    """
    Show recent history
    """
    _print_recent_history(
        _recent_history_entries(limit=limit, history_type=history_type)
    )


def _rate_input(input: Input, rating: int) -> None:
    if isinstance(input, MovieId):
        mv = input.trakt()
        _print_response(mv.rate(rating), rating=True)
    elif isinstance(input, EpisodeId):
        ep = input.trakt()
        _print_response(ep.rate(rating), rating=True)
    elif isinstance(input, TVShowId):
        tv = input.trakt()
        _print_response(tv.rate(rating), rating=True)
    else:
        raise ValueError(f"Invalid input type: {type(input)}")


@main.command(short_help="rate movie/tv show/episode")
@click.option(
    "--url",
    "inp",
    help="URL to rate",
    default=None,
    type=str,
    callback=_handle_input,
)
@click.option(
    "-r",
    "--rating",
    help="Rating",
    type=click.IntRange(min=1, max=10),
    required=True,
    prompt=True,
)
def rate(inp: Input, rating: int) -> None:
    """
    Pass the movie/TV show/episode url to rate it
    """
    _rate_input(inp, rating)


if __name__ == "__main__":
    main(prog_name="trakt-watch")
