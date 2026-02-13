pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'chateniumadw'
gnome = import('gnome')
python = import('python')

blueprints = custom_target('blueprints',
  input: files(
    'views/window.blp',
    'views/login/login.blp',
    'views/chat/chat.blp',
    'views/chat/dm/dm.blp',
    'views/chat/elements/message/message.blp',
    'views/chat/elements/message_box/message_box.blp',
    'views/chat/elements/message_box/message_box_dialog.blp'
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
  'views/global.css',
  'views/login/__init__.py',
  'views/login/login.py',
  'views/login/login.css',
  'views/chat/chat.py',
  'viewmodel/chat/chat_model.py',
  'views/async_image.py',
  'views/async_image_scaled.py',
  'views/chat/dm/dm.py',
  'views/chat/dm/dm.css',
  'views/chat/elements/message/message.py',
  'views/chat/elements/message/message.css',
  'views/chat/elements/message_box/message_box.py',
  'views/chat/elements/message_box/message_box_dialog.py',
  'viewmodel/chat/elements/message_box/message_box_model.py',
  'viewmodel/chat/dm/dm_model.py'
]

install_data(chateniumadw_sources, install_dir: moduledir)
