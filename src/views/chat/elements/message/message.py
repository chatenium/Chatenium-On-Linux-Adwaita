from gi.repository import Adw, Gtk, Gdk, GLib, GObject
import os
from backend.session_manager import SessionManager

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

        gesture = Gtk.GestureClick.new()
        gesture.set_button(Gdk.BUTTON_SECONDARY)
        gesture.connect("pressed", self.on_right_click)
        self.add_controller(gesture)

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
