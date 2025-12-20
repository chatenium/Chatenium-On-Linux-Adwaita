from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gdk
from .login_model import login, AuthMethodResp
import os
import asyncio
import threading

@Gtk.Template(resource_path='/hu/chatenium/chtnoladw/views/login/login.ui')
class LoginView(Gtk.Box):
    __gtype_name__ = 'LoginView'

    login_button = Gtk.Template.Child()
    first_page = Gtk.Template.Child()
    second_page = Gtk.Template.Child()
    username_field = Gtk.Template.Child()
    stack = Gtk.Template.Child()

    password_auth = Gtk.Template.Child()
    email_auth = Gtk.Template.Child()
    sms_auth = Gtk.Template.Child()

    def __init__(self, toast_overlay, **kwargs):
        super().__init__(**kwargs)
        self.toast_overlay = toast_overlay
        self.add_styles()

    @Gtk.Template.Callback()
    def get_auth_callback(self, button):
        print("Login clicked")
        username = self.username_field.get_text()
        threading.Thread(
            target=lambda: asyncio.run(self._get_auth(username)),
            daemon=True,
        ).start()

    async def _get_auth(self, username):
        try:
            result = await login(username)
            print("Got auth options")
            self.stack.set_visible_child_name("second_page")
            self.password_auth.set_visible(result.password)
            self.email_auth.set_visible(result.email)
            self.sms_auth.set_visible(result.sms)
        except Exception as e:
            toast = Adw.Toast.new(_("The server has returned an error"))
            print(e)
            self.toast_overlay.add_toast(toast)

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
