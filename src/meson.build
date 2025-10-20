pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'chateniumadw'
gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'views/window.blp',
    'views/login/login.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('chateniumadw',
  'chateniumadw.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: blueprints,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'chateniumadw.in',
  output: 'chateniumadw',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x'
)

chateniumadw_sources = [
  '__init__.py',
  'main.py',
  'views/__init__.py',
  'views/window.py',
  'views/login/__init__.py',
  'views/login/login.py',
  'views/login/login.css',
  'backend/backend_tester.py',
  'backend/login/login_model.py',
  'backend/environments.py',
  'backend/shared/local_storage.py',
]

install_data(chateniumadw_sources, install_dir: moduledir)
