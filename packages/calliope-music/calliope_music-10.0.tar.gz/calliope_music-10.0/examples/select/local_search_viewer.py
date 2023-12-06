"""Demo of the Calliope `select` module."""

from simpleai.search.viewers import ConsoleViewer, WebViewer

from calliope.playlist import Playlist, PlaylistItem
from calliope.select import ItemDurationConstraint, PlaylistDurationConstraint
import calliope.playlist
import calliope.select
import calliope.shuffle

import sys

MINUTES = 60


corpus = Playlist([
    PlaylistItem({"calliope.id": "👸", "title": "Amazing Tune", "duration": 2 * MINUTES}),
    PlaylistItem({"calliope.id": "🎸", "title": "Punk Classic", "duration": 1 * MINUTES}),
    PlaylistItem({"calliope.id": "♬", "title": "Lengthy Opus", "duration": 12 * MINUTES}),
    PlaylistItem({"calliope.id": "🌄", "title": "Ambient Noise", "duration": 7 * MINUTES}),
])

constraints = [
    ItemDurationConstraint(vmin=2 * MINUTES,vmax=4 * MINUTES),
    PlaylistDurationConstraint(vmin=10 * MINUTES,vmax=10 * MINUTES),
]

#viewer = WebViewer()
viewer = ConsoleViewer()
input_playlist = calliope.shuffle.shuffle(corpus)
output_playlist = calliope.select.select(input_playlist, constraints, viewer=viewer)

calliope.playlist.write(output_playlist, sys.stdout)
sys.stderr.write(f"Total playlist duration: {sum(item['duration'] for item in output_playlist)}\n")
#web_viewer_server.run_server(web_viewer)
