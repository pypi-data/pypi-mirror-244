# Calliope
# Copyright (C) 2016,2018,2020  Sam Thursfield <sam@afuera.me.uk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""Export data from the `Tracker desktop search engine <gnome.pages.gitlab.gnome.org/tracker/>`_.

See also: :program:`cpe tracker` command.

"""

import gi

try:
    gi.require_version("MediaArt", "2.0")
    gi.require_version("Tracker", "3.0")
    from gi.repository import MediaArt, Tracker  # pylint: disable=no-name-in-module
except ValueError as e:
    raise ImportError(e) from e

from calliope.interface import ContentResolver
import calliope.playlist

import logging
from pathlib import Path
import re
import urllib.parse

log = logging.getLogger(__name__)

TRACKER_INDEXER = "org.freedesktop.Tracker3.Miner.Files"


def _escape(s):
    return Tracker.sparql_escape_string(s)


class TrackerClient(ContentResolver):
    """Helper functions for querying from the user's Tracker database.

    This class caches a TrackerSparqlConnection and prepared SPARQL statements.
    For that reason it should only be used from a single thread. Create
    multiple instances if you need to use this from multiple threads.
    """

    QUERIES_PATH = Path(__file__).parent.joinpath("queries")

    # We can't make `LIMIT` optional based on a parameter, instead we use a
    # very high limit.
    MAX_ROW_COUNT = 2**63

    def __init__(self, http_endpoint=None):
        if http_endpoint:
            self._conn = Tracker.SparqlConnection.remote_new(http_endpoint)
        else:
            self._conn = Tracker.SparqlConnection.bus_new(TRACKER_INDEXER, None, None)

        self._stmt_cache = {}

    def authenticate(self):
        """No-op as this is a local service."""
        pass

    def query(self, query: str) -> Tracker.SparqlCursor:
        """Run a single SPARQL query."""
        log.debug("Query: %s" % query)
        return self._conn.query(query)

    def _stored_query(self, name):
        if name not in self._stmt_cache:
            # Get stored query from `queries/` directory. Load and prepare on
            # demand, caching the TrackerSparqlStatement so compilation only
            # happens once.
            sparql = self.QUERIES_PATH.joinpath(name).with_suffix(".rq").read_text()
            self._stmt_cache[name] = self._conn.query_statement(sparql, None)
        return self._stmt_cache[name]

    def _execute_statement(
        self,
        statement: Tracker.SparqlStatement,
        **bindings,
    ) -> Tracker.SparqlCursor:
        log.debug(
            "Running statement.\nSPARQL: %s.\nBindings: %s.\n",
            statement.get_sparql(),
            bindings,
        )
        statement.clear_bindings()
        for key, value in bindings.items():
            if isinstance(value, bool):
                # This is a workaround for
                # https://gitlab.gnome.org/GNOME/tracker/-/issues/417
                statement.bind_string(key, "true" if value else "false")
            elif isinstance(value, int):
                statement.bind_integer(key, value)
            elif isinstance(value, str):
                statement.bind_string(key, value)
            else:
                raise ValueError(f"Unsupported value type for binding: {value} ({type(value)})")
        return statement.execute()

    def _execute_stored_query(self, name: str, **bindings):
        return self._execute_statement(self._stored_query(name), **bindings)

    def artist_id(self, artist_name: str) -> str:
        """Return the Tracker URN for a given artist."""
        result = self._execute_stored_query(
            "lookup_artist_by_name",
            name=artist_name
        )
        if result.next():
            return result.get_string(0)[0]
        else:
            return None

    def artist_name(self, artist_id: str) -> str:
        """Return the name of a given artist."""
        result = self._execute_stored_query(
            "get_artist_name",
            artist_urn=artist_id,
        )
        if result.next():
            return result.get_string(0)[0]
        else:
            return None

    def artists_by_number_of_songs(self, limit: int = None):
        """Return a list of artists by number of songs known."""
        cursor = self._execute_stored_query(
            "get_artist_track_count",
            limit=limit or self.MAX_ROW_COUNT,
        )
        while cursor.next():
            artist_name = cursor.get_string(0)[0]
            n_songs = cursor.get_string(1)[0]
            yield {"artist": artist_name, "track-count": n_songs}

    def albums(self, filter_artist_name: str = None, filter_album_name: str = None):
        """Return a list of releases."""

        stmt = self._stored_query("albums")

        parameters = {
            "all_artists": True,
            "all_albums": True,
            "artist_name": "",
            "album_name": "",
        }
        if filter_artist_name:
            parameters["all_artists"] = False
            parameters["artist_name"] = filter_artist_name

        if filter_album_name:
            parameters["all_albums"] = False
            parameters["album_name"] = filter_album_name

        count = 0
        albums = self._execute_statement(stmt, **parameters)
        while albums.next():
            log.debug("Got 1 result")
            track_uri = albums.get_string(2)[0]
            track_path = urllib.parse.unquote(urllib.parse.urlparse(track_uri).path)
            album_path = Path(track_path).parent
            yield {
                "creator": albums.get_string(0)[0],
                "album": albums.get_string(1)[0],
                "location": album_path.as_uri(),
                "tracker.location": album_path.as_uri(),
                "album.trackcount": albums.get_integer(3),
                "tracker.size_mb": round(albums.get_double(4)),
                "duration": albums.get_integer(5) * 1000,
            }
            count += 1
        log.debug("Got %i results", count)

    @staticmethod
    def _fts_safe_string(name):
        # Prepare a set of terms that will work with Tracker FTS engine.
        # The result may be an empty string.
        result = []
        punctation_within_word=re.compile(r"\b\w+(\W+)\w*")
        strip_symbols=re.compile(r"\W")
        words = name.split(" ")
        for word in words:
            symbol_match = punctation_within_word.match(word)
            if symbol_match:
                # Symbols in words can fail to match, there are bugs here
                # in Tracker. See:
                # https://gitlab.gnome.org/GNOME/tracker/-/issues/400
                break
            else:
                (stripped, _count) = strip_symbols.subn("", word)
                if len(stripped) > 0:
                    result.append(stripped)
        return " ".join(result)

    def track(self, artist_name: str, track_name: str) -> calliope.playlist.Item:
        """Find a specific track by name.

        Tries to find a track matching the given artist and title.

        Returns a playlist entry, or None.

        """

        track_name_fts = self._fts_safe_string(track_name)
        artist_name_fts = self._fts_safe_string(artist_name)

        if track_name_fts and artist_name_fts:
            # The FTS query is much faster than the FILTER-based query, but
            # cannot always be used due to limitations of the Tracker SPARQL
            # FTS engine.
            cursor = self._execute_stored_query(
                "lookup_track_by_name_fts",
                track_name_fts=track_name_fts,
                artist_name_fts=artist_name_fts,
                track_name=track_name,
                artist_name=artist_name,
            )
        else:
            cursor = self._execute_stored_query(
                "lookup_track_by_name",
                track_name=track_name,
                artist_name=artist_name,
            )
        if cursor.next():
            return calliope.playlist.Item(
                {
                    "title": track_name,
                    "creator": artist_name,
                    "location": cursor.get_string(0)[0],
                    "tracker.location": cursor.get_string(0)[0],
                    "duration": cursor.get_integer(1) * 1000,
                }
            )
        else:
            return calliope.playlist.Item()

    def tracks(
        self, filter_artist_name: str = None, filter_album_name: str = None
    ) -> calliope.playlist.Playlist:
        """Return a list of tracks."""
        stmt = self._stored_query("tracks")

        parameters = {
            "all_artists": True,
            "all_albums": True,
            "artist_name": "",
            "album_name": "",
        }
        if filter_artist_name:
            parameters["all_artists"] = False
            parameters["artist_name"] = filter_artist_name.lower()

        if filter_album_name:
            parameters["all_albums"] = False
            parameters["album_name"] = filter_album_name.lower()

        count = 0
        tracks = self._execute_statement(stmt, **parameters)
        while tracks.next():
            log.debug("Got 1 result")
            item = calliope.playlist.Item(
                {
                    "title": tracks.get_string(0)[0],
                    "creator": tracks.get_string(2)[0],
                    "location": tracks.get_string(1)[0],
                    "tracker.location": tracks.get_string(1)[0],
                    "tracker.size_mb": round(tracks.get_double(3)),
                    "duration": tracks.get_integer(4) * 1000,
                }
            )
            album = tracks.get_string(5)[0]
            if album:
                item["album"] = album

            yield item

            count += 1
        log.debug("Got %i results", count)

    def tracks_grouped_by_album(
        self,
        filter_artist_name: str = None,
        filter_album_name: str = None,
        filter_track_name: str = None,
    ) -> calliope.playlist.Playlist:
        """Return all songs matching specific search criteria.

        These are grouped into their respective releases. Any tracks that
        aren't present on any releases will appear last. Any tracks that
        appear on multiple releases will appear multiple times.

        """
        parameters = {
            "all_artists": True,
            "all_tracks": True,
            "artist_urn": "",
            "tracks_name": "",
        }

        parameters_album = {
            "all_albums": True,
            "album_name": "",
        }

        if filter_artist_name:
            artist_id = self.artist_id(filter_artist_name)
            parameters["all_artists"] = False
            parameters["artist_urn"] = artist_id

        if filter_track_name:
            parameters["all_tracks"] = False
            parameters["track_name"] = filter_track_name

        if filter_album_name:
            parameters_album["all_albums"] = False
            parameters_album["album_name"] = filter_album_name

        songs_with_releases = self._execute_stored_query(
            "tracks_grouped_by_album",
            **(parameters_album + parameters)
        )

        if filter_album_name:
            songs_without_releases = None
        else:
            songs_without_releases = self._execute_stored_query(
                "tracks_without_albums", **parameters
            )

        while songs_with_releases.next():
            artist_name = filter_artist_name or songs_with_releases.get_string(4)[0]
            album_name = songs_with_releases.get_string(0)[0]
            if songs_with_releases.is_bound(3):
                tracknum = songs_with_releases.get_integer(3)
            else:
                tracknum = None

            item = {
                "album": album_name,
                "creator": artist_name,
                "location": songs_with_releases.get_string(1)[0],
                "title": songs_with_releases.get_string(2)[0],
            }
            if tracknum:
                item["trackNum"] = tracknum
            yield item

        if songs_without_releases:
            while songs_without_releases.next():
                artist_name = (
                    filter_artist_name or songs_without_releases.get_string(3)[0]
                )
                yield calliope.playlist.Item(
                    {
                        "creator": artist_name,
                        "location": songs_without_releases.get_string(0)[0],
                        "title": songs_without_releases.get_string(2)[0],
                    }
                )

    def artists(self) -> calliope.playlist.Playlist:
        """Return all artists who have at least one track available locally."""
        artists_with_tracks = self._execute_stored_query("artists_with_tracks")
        count = 0
        while artists_with_tracks.next():
            log.debug("Got 1 result")
            artist_name = artists_with_tracks.get_string(0)[0]
            yield calliope.playlist.Item(
                {
                    "creator": artist_name,
                }
            )
            count += 1
        log.debug("Got %i results", count)

    def search(self, search_text: str) -> calliope.playlist.Playlist:
        """Return a list of tracks which match 'search_text'.

        The text may be matched in the artist name, track title or album name.
        """

        tracks = self._execute_stored_query("search", text=_escape(search_text))
        while tracks.next():
            yield calliope.playlist.Item(
                {
                    "title": tracks.get_string(0)[0],
                    "creator": tracks.get_string(2)[0],
                    "location": tracks.get_string(1)[0],
                    "tracker.location": tracks.get_string(1)[0],
                }
            )

    def _resolve_item(self, item: calliope.playlist.Item) -> calliope.playlist.Item:
        item = calliope.playlist.Item(item)
        if "title" not in item or "creator" not in item:
            return item.add_warning(
                "tracker", "Cannot set location -- no title or creator info"
            )

        tracker_item = self.track(artist_name=item["creator"], track_name=item["title"])

        if tracker_item:
            item.update(tracker_item)
        else:
            item.add_warning("tracker", "Cannot set location -- track not found")

        return item

    def resolve_content(
        self, playlist: calliope.playlist.Playlist
    ) -> calliope.playlist.Playlist:
        """Resolve content locations from the local filesystem."""
        for item in playlist:
            try:
                item = self._resolve_item(item)
            except RuntimeError as e:
                raise RuntimeError("%s\nItem: %s" % (e, item)) from e

            if "tracker.location" in item and "location" not in item:
                item["location"] = item["tracker.location"]

            yield item


def annotate_images(
    tracker: TrackerClient, playlist: calliope.playlist.Playlist
) -> calliope.playlist.Playlist:
    """Resolve images from local media-art cache."""
    playlist = list(playlist)
    for item in playlist:
        if "title" in item and "creator" in item:
            image_file = MediaArt.get_file(item["creator"], item["title"], "track")[1]
            if image_file.query_exists():
                item["tracker.track_image"] = image_file.get_uri()
        if "album" in item and "creator" in item:
            image_file = MediaArt.get_file(item["creator"], item["album"], "album")[1]
            if image_file.query_exists():
                item["tracker.album_image"] = image_file.get_uri()
        yield item


def resolve_content(
    tracker: TrackerClient, playlist, *args, **kwargs
) -> calliope.playlist.Playlist:
    """Resolve content locations from the local filesystem."""
    return tracker.resolve_content(playlist, *args, **kwargs)


def resolve_image(
    tracker: TrackerClient, playlist: calliope.playlist.Playlist
) -> calliope.playlist.Playlist:
    """Resolve ``image`` from local media-art cache."""
    playlist = list(playlist)
    for item in playlist:
        if "image" not in item:
            if "album" in item and "creator" in item:
                image_file = MediaArt.get_file(item["creator"], item["album"], "album")[
                    1
                ]
                if image_file.query_exists():
                    item["image"] = image_file.get_uri()
        if "image" not in item:
            if "title" in item and "creator" in item:
                image_file = MediaArt.get_file(item["creator"], item["title"], "track")[
                    1
                ]
                if image_file.query_exists():
                    item["image"] = image_file.get_uri()
        yield item


def expand_tracks(
    tracker: TrackerClient, playlist: calliope.playlist.Playlist
) -> calliope.playlist.Playlist:
    """Expand an ``album`` item into a list of the album's tracks."""
    for item in playlist:
        if "title" in item:
            yield item
        elif "album" in item:
            yield from tracker.tracks(
                filter_artist_name=item["creator"], filter_album_name=item["album"]
            )
        else:
            yield from tracker.tracks(filter_artist_name=item["creator"])
