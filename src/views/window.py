from gi.repository import Adw
from gi.repository import Gtk
from .login import LoginView
from .backend_tester import Test

@Gtk.Template(resource_path='/hu/chatenium/chtnoladw/views/window.ui')
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MainWindow'

    label = Gtk.Template.Child()
    testButton = Gtk.Template.Child()
    view_stack = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.testButton.connect("clicked", self.navigate)

    def navigate(self, button):
        self.view_stack.add_titled(LoginView(), "login_view", "login_view")
        self.view_stack.set_visible_child_name("login_view")
        te = Test()
        te.fodiJozsi()
