FROM fedora:39

RUN dnf install -y dbus-x11 dconf glib2-devel gstreamer1-plugins-good libmediaart-devel ninja-build python3-gobject python3-pip python3-pylint python3-pytest python3-pytest-benchmark python3-pyyaml rsync tracker3-devel tracker3-miners && \
      pip3 install meson && \
      pip3 install click jsonlines jsonschema parsedatetime && \
      pip3 install mutagen && \
      pip3 install beautifulsoup4 cachecontrol google-api-python-client jinja2 lastfmclient lockfile lxml musicbrainzngs pylistenbrainz simpleai spotipy && \
      pip3 install sphinx sphinx-autoapi sphinx-click sphinx-jsonschema && \
      pip3 install coverage pytest-cov pytest-pep8 && \
      rm -R /root
RUN dnf install -y git
RUN pip install git+https://gitlab.com/samthursfield/calliope/
