Notes for developers working on Calliope itself
===============================================

Tests for web service integration
---------------------------------

Automated tests should not run against a real web service, for reliability
and performance reasons. Here are examples of how web APIs can be mocked in Calliope test
suite. There are several methods, as most integrations use a third-party helper library
rather than talking directly to the remote service.

Run a local HTTP server
~~~~~~~~~~~~~~~~~~~~~~~

This method is used by ``test_lastfm_history.py``.
Python ``wsgiref.simple_server`` runs a real HTTP server, and the address is
passed to ``cpe lastfm-history`` command with the ``--server`` argument.

Override the urllib Opener class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method is used by ``test_musicbrainz.py``, adapted from the testsuite of
the Python ``musicbrainzngs`` module. An internal function from ``musicbrainzngs``
is monkeypatched to use our custom URL opener. Testcases supply a map of URL
patterns as regular expressions and functions which simulate the response.

Override the public API of the client library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method is used by ``test_spotify.py``. The whole :class:`calliope.spotify.SpotifyContext`
class is replaced with a ``unittest.mock.Mock`` instance, allowing us to replace the Spotipy client
library completely with our own functions.

Tracker module: debugging test failures
---------------------------------------

Reproducing test failures from the `test_tracker_search` test is not trivial.

First, modify the `tracker_miner_fs_sandbox()` fixture and comment the `rmtree` calls so the
test data is preserved, and print its location.

Now, you can use the `tracker3` CLI commands such as `export` and `sparql` to inspect the
store. If the store tmpdir was `tmp/tracker-indexed-tmpdirerdtqnw9/` you could run this
to dump all data:

    tracker3 export --database /tmp/tracker-indexed-tmpdirerdtqnw9/cache/tracker3/files/

You can also use the `tracker-sandbox` utility with the --store and
--index-recursive-directories options to open a shell with running Tracker
Miners process which you can run `cpe` commands against.
