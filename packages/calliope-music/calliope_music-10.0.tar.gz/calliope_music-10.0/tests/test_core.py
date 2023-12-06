# Calliope
# Copyright (C) 2019  Sam Thursfield <sam@afuera.me.uk>
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


import jsonlines
import pytest

import io
import json

from calliope.playlist import PlaylistError
import calliope.playlist


def text_to_stream(text):
    return io.BytesIO(text.encode("utf-8"))


def test_playlist_json_stream(cli):
    """Test reading playlist as a sequence of space-separated JSON objects.

    This format is tricky because the stream as a whole is not a valid
    JSON document. See https://stackoverflow.com/q/6886283/10433384 for some
    background.

    """
    item_a = {"artist": "a"}
    item_text = ' { "artist": "a" } '

    text = item_text
    result = calliope.playlist.read(text_to_stream(text))
    assert list(result) == [item_a]

    text = "\n".join([item_text] * 3)
    result = calliope.playlist.read(text_to_stream(text))
    assert list(result) == [item_a] * 3


def test_playlist_json_document(cli):
    """Test reading playlist as a JSON document."""

    playlist = [
        {"artist": "a"},
        {"artist": "b"},
    ]

    text = json.dumps(playlist)
    result = calliope.playlist.read(text_to_stream(text))
    assert list(result) == playlist

    # jsonlines considers the input invalid if there's a line which is not
    # a complete JSON object, and that is correct behaviour.
    text = json.dumps(playlist, indent=4)
    with pytest.raises(PlaylistError):
        result = calliope.playlist.read(text_to_stream(text))
        assert list(result) == playlist


def test_split_playlist():
    track_a1 = {"playlist.title": "A", "track": "A1"}
    track_a2 = {"track": "A2"}
    track_b1 = {"playlist.title": "B", "track": "B1"}

    playlist_stream = [track_a1, track_a2, track_b1]

    result = list(calliope.playlist.split(playlist_stream))
    assert len(result) == 2
    assert list(result[0]) == [track_a1, track_a2]
    assert list(result[1]) == [track_b1]
