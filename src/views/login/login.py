from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gdk
import os

@Gtk.Template(resource_path='/hu/chatenium/chtnoladw/views/login/login.ui')
class LoginView(Gtk.Box):
    __gtype_name__ = 'LoginView'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_styles()

    def add_styles(self):
        css_provider = Gtk.CssProvider()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        css_file_path = os.path.join(current_dir, "login.css")
        css_provider.load_from_path(css_file_path)
        print("CSS for loginView loaded.")
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )
