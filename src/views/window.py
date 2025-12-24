from gi.repository import Adw
from gi.repository import Gtk
from .login import LoginView
from .chat import ChatView
from backend.session_manager import SessionManager
from backend.environments import Environments

@Gtk.Template(resource_path='/hu/chatenium/chtnoladw/views/window.ui')
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MainWindow'

    label = Gtk.Template.Child()
    testButton = Gtk.Template.Child()
    view_stack = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        print(Environments)
        Environments.instance().overwrite_env("http://192.168.1.228:3000", "ws://192.168.1.228:3000")

        signedIn = SessionManager.instance().loadSessions()
        if signedIn:
            self.view_stack.add_titled(ChatView(), "chat_view", "chat_view")
            self.view_stack.set_visible_child_name("chat_view")
        else:
            self.view_stack.add_titled(LoginView(self.toast_overlay, self.view_stack), "login_view", "login_view")
            self.view_stack.set_visible_child_name("login_view")


