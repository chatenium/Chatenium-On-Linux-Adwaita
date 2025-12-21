from gi.repository import Adw
from gi.repository import Gtk

@Gtk.Template(resource_path='/hu/chatenium/chtnoladw/views/chat/chat.ui')
class ChatView(Gtk.Box):
    __gtype_name__ = 'ChatView'
