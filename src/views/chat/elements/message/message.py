from gi.repository import Adw, Gtk, Gdk, GLib, GObject, Gio
import os
from backend.session_manager import SessionManager
from .async_image_scaled import AsyncImageScaled
from pathlib import Path
import urllib
import requests

@Gtk.Template(resource_path='/hu/chatenium/chtnoladw/views/chat/elements/message/message.ui')
class MessageElement(Gtk.Box):
    __gtype_name__ = 'MessageElement'
    __gsignals__ = {
        "request-message-management": (GObject.SIGNAL_RUN_FIRST, None, (object,str)),
        "request-message-delete": (GObject.SIGNAL_RUN_FIRST, None, (object,))
    }

    main_message = Gtk.Template.Child()
    popover = Gtk.Template.Child()
    holder_box = Gtk.Template.Child()
    popover_reply = Gtk.Template.Child()
    popover_edit = Gtk.Template.Child()
    popover_delete = Gtk.Template.Child()
    reply_to = Gtk.Template.Child()
    reply_to_label = Gtk.Template.Child()
    attachments_list = Gtk.Template.Child()

    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.main_message.set_label(message.message)
        self.add_styles()

        self.is_author = True
        if SessionManager.instance().currentSession[1].userid != message.author:
            self.is_author = False
            self.holder_box.add_css_class("message_is_not_author")

        if message.replyTo != "":
            self.reply_to.set_visible(True)
            self.reply_to_label.set_label(message.replyTo)

        self._load_attachments(message.files)

        gesture = Gtk.GestureClick.new()
        gesture.set_button(Gdk.BUTTON_SECONDARY)
        gesture.connect("pressed", self.on_right_click)
        self.add_controller(gesture)

    def _load_attachments(self, attachments):
        if attachments:
            self.attachments_list.set_visible(True)

            for attachment in attachments:
                if attachment.type == "image":
                    max_size = 300
                    scale_w = max_size / attachment.width
                    scale_h = max_size / attachment.height
                    scale = min(scale_w, scale_h)

                    new_width = int(attachment.width * scale)
                    new_height = int(attachment.height * scale)

                    img = AsyncImageScaled(attachment.path, new_height, new_width)

                    # Add click gesture
                    click = Gtk.GestureClick.new()
                    click.connect("pressed", self.on_image_clicked, attachment)

                    img.add_controller(click)

                    self.attachments_list.append(img)

    def on_image_clicked(self, gesture, n_press, x, y, attachment):
        print(f"Image clicked! Path: {attachment.path}")
        downloads = Path.home() / "Downloads"
        downloads.mkdir(exist_ok=True)
        safe_url = urllib.parse.quote(attachment.path, safe=':/')
        response = requests.get(safe_url)
        response.raise_for_status()  # raise error if request fails
        file_path = downloads / attachment.fileName
        with open(file_path, "wb") as f:
            f.write(response.content)
        uri = Gio.File.new_for_path(str(file_path)).get_uri()
        Gio.AppInfo.launch_default_for_uri(uri, None)

    def on_right_click(self, gesture, n_press, x, y):
        if self.is_author:
            self.popover_reply.set_visible(False)
            self.popover_edit.set_visible(True)
            self.popover_delete.set_visible(True)
        else:
            self.popover_reply.set_visible(True)
            self.popover_edit.set_visible(False)
            self.popover_delete.set_visible(False)
        self.popover.set_parent(self)
        self.popover.popup()

    @Gtk.Template.Callback()
    def mark_message_for_edit(self, button):
        self.emit("request-message-management", self.message, "edit")

    @Gtk.Template.Callback()
    def mark_message_for_delete(self, button):
        self.emit("request-message-delete", self.message)

    @Gtk.Template.Callback()
    def mark_message_for_reply(self, button):
        self.emit("request-message-management", self.message, "reply")

    def add_styles(self):
        css_provider = Gtk.CssProvider()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        css_file_path = os.path.join(current_dir, "message.css")
        css_provider.load_from_path(css_file_path)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

