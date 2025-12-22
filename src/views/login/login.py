from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gdk
from backend.login.login_model import login, AuthMethodResp, password_auth, otp_send_code, otp_verify_code
from backend.session_manager import User
from urllib.parse import quote, quote_plus

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
    password_field = Gtk.Template.Child()
    email_code_field = Gtk.Template.Child()
    sms_code_field = Gtk.Template.Child()

    identity = ""

    def __init__(self, toast_overlay, **kwargs):
        super().__init__(**kwargs)
        self.toast_overlay = toast_overlay

    @Gtk.Template.Callback()
    def get_auth_callback(self, button):
        print("Login clicked")
        username = self.username_field.get_text()
        self.identity = username
        threading.Thread(
            target=lambda: asyncio.run(self._get_auth(quote_plus(username))),
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
            self.toast_overlay.add_toast(toast)

    ### Password auth
    @Gtk.Template.Callback()
    def use_password_auth(self, button):
        print("clicked")
        self.stack.set_visible_child_name("password_auth")

    @Gtk.Template.Callback()
    def signin_with_password(self, button):
        print("Signing in with password")
        password = self.password_field.get_text()
        threading.Thread(
            target=lambda: asyncio.run(self._do_signin_with_password(password)),
            daemon=True
        ).start()

    async def _do_signin_with_password(self, password):
        try:
            result = await password_auth(self.identity, password)
            print(result)
        except Exception as e:
            toast = Adw.Toast.new(_("Incorrect password"))
            self.toast_overlay.add_toast(toast)

    ### E-Mail auth
    @Gtk.Template.Callback()
    def use_email_auth(self, button):
        threading.Thread(
            target=lambda: asyncio.run(self._do_send_otp_code(1, self.identity)),
            daemon=True
        ).start()

    @Gtk.Template.Callback()
    def signin_with_email_code(self, button):
        threading.Thread(
            target=lambda: asyncio.run(self._do_verify_otp_code(1, self.identity, self.email_code_field.get_text())),
            daemon=True
        ).start()

    ### SMS auth
    @Gtk.Template.Callback()
    def use_sms_auth(self, button):
        threading.Thread(
            target=lambda: asyncio.run(self._do_send_otp_code(0, self.identity)),
            daemon=True
        ).start()

    @Gtk.Template.Callback()
    def signin_with_sms_code(self, button):
        threading.Thread(
            target=lambda: asyncio.run(self._do_verify_otp_code(0, self.identity, self.sms_code_field.get_text())),
            daemon=True
        ).start()

    async def _do_send_otp_code(self, type: int, to: str):
        try:
            await otp_send_code(type, to)
            self.stack.set_visible_child_name("email_auth" if (type == 1) else "sms_auth")
        except Exception as e:
            toast = Adw.Toast.new(f"{e}")
            self.toast_overlay.add_toast(toast)

    async def _do_verify_otp_code(self, type: int, to: str, code: str):
        try:
            await otp_verify_code(type, to, int(code))
        except Exception as e:
            toast = Adw.Toast.new(f"{e}")
            self.toast_overlay.add_toast(toast)
"""
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
"""
