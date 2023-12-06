sources = files('__init__.py')

python.install_sources(
    sources,
    subdir: 'calliope/tracker')

install_subdir(
  'queries',
  install_dir: python.get_install_dir() / 'calliope' / 'tracker'
)

calliope_module_sources += sources
