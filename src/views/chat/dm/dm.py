from gi.repository import Adw, Gtk, Gdk
import os

@Gtk.Template(resource_path='/hu/chatenium/chtnoladw/views/chat/dm/dm.ui')
class DmView(Gtk.Box):
    __gtype_name__ = 'DmView'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_styles()

    def add_styles(self):
        css_provider = Gtk.CssProvider()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        css_file_path = os.path.join(current_dir, "dm.css")
        css_provider.load_from_path(css_file_path)
        print("CSS for DmView loaded.")
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )
