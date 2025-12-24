pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'chateniumadw'
gnome = import('gnome')
python = import('python')
pip = find_program('pip3')

backend_install = custom_target(
  'backend_install',
  output: 'b',
  command: [
    'sh', '-c',
    'pip3 install --user git+https://github.com/chatenium/Chatenium-On-Linux-UniEnd'
  ]
)

blueprints = custom_target('blueprints',
  input: files(
    'views/window.blp',
    'views/login/login.blp',
    'views/chat/chat.blp',
    'views/chat/dm/dm.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
  depends: backend_install
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
  'views/chat/chat.py',
  'views/async_image.py',
  'views/chat/dm/dm.py',
  'views/chat/dm/dm.css',
]

install_data(chateniumadw_sources, install_dir: moduledir)
