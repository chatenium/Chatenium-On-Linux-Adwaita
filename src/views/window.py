from gi.repository import Adw, Gtk, Gdk
from .login import LoginView
from .chat import ChatView
from backend.session_manager import SessionManager
from backend.environments import Environments
import os

@Gtk.Template(resource_path='/hu/chatenium/chtnoladw/views/window.ui')
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MainWindow'

    label = Gtk.Template.Child()
    testButton = Gtk.Template.Child()
    view_stack = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #print(Environments)
        #print("Overwritten")
        print("Setting envs")
        # Environments.instance().overwrite_env("http://192.168.1.228:3000", "ws://192.168.1.228:3000")
        print(Environments)

        css_provider = Gtk.CssProvider()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        css_file_path = os.path.join(current_dir, "global.css")
        css_provider.load_from_path(css_file_path)
        print("Global styles file loaded.")
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        signedIn = SessionManager.instance().loadSessions()
        if signedIn:
            self.view_stack.add_titled(ChatView(), "chat_view", "chat_view")
            self.view_stack.set_visible_child_name("chat_view")
        else:
            self.view_stack.add_titled(LoginView(self.toast_overlay, self.view_stack), "login_view", "login_view")
            self.view_stack.set_visible_child_name("login_view")
