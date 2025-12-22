from gi.repository import Adw
from gi.repository import Gtk

@Gtk.Template(resource_path='/hu/chatenium/chtnoladw/views/chat/chat_row.ui')
class ChatRow(Gtk.ListBoxRow):
    __gtype_name__ = "ChatRow"
