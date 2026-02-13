from gi.repository import Adw, Gtk, Gdk, GLib
from backend.chat.dm.dm_handler import DmHandler, Attachment
from backend.session_manager import SessionManager
from .message import MessageElement
from .message_box_model import MessageBoxViewModel
import os
import threading
import asyncio
import time
from .message_box import MessageBox
from .dm_model import DmViewModel

@Gtk.Template(resource_path='/hu/chatenium/chtnoladw/views/chat/dm/dm.ui')
class DmView(Gtk.Box):
    __gtype_name__ = 'DmView'

    view_model = None
    message_list_factory = Gtk.SignalListItemFactory()

    message_list_holder = Gtk.Template.Child()
    message_list = Gtk.Template.Child()
    message_list_loader = Gtk.Template.Child()
    message_list_view = Gtk.Template.Child()

    msg_box = Gtk.Template.Child()

    message_management_type = None

    def __init__(self, chat, **kwargs):
        super().__init__(**kwargs)
        self.message_list_holder.set_visible_child(self.message_list_loader)
        self.message_list_loader.start()
        self.chatdata = chat
        self.add_styles()

        # Initialize view model
        self.view_model = DmViewModel(chat)

        # Create binding for message list
        self.message_list_factory.connect("setup", self._message_list_factory_setup)
        self.message_list_factory.connect("bind", self._message_list_factory_bind)
        self.message_list_view.set_factory(self.message_list_factory)
        selection_model = Gtk.NoSelection(model=self.view_model.messages)
        self.message_list_view.set_model(selection_model)

        # Load messages and show them
        self.view_model.load_messages()
        self.message_list_holder.set_visible_child(self.message_list)

        threading.Thread(
            target=lambda: asyncio.run(self.view_model.join_chat()),
            daemon=True
        ).start()

        # Message Box
        message_box = MessageBox(view_model=self.view_model.message_box_view_model)
        message_box.connect("message-sent", self._message_sent_event)
        self.msg_box.append(message_box)

    def _message_list_factory_setup(self, factory, list_item):
        row = MessageElement()
        row.connect("request-message-management", self._set_message_for_management)
        row.connect("request-message-delete", self._set_message_for_deletion)
        list_item.row = row
        list_item.set_child(row)
        GLib.timeout_add_seconds(1, self._scroll_to_bottom)

    def _message_list_factory_bind(self, factory, list_item):
        message: MessageAdapter = list_item.get_item()
        list_item.row.init_element(message)

    def _set_message_for_management(self, child, message, mtype):
        # Data for later
        self.view_model.message_box_view_model.management_data = message
        self.view_model.message_box_view_model.management_type = mtype
        self.view_model.message_box_view_model.management_box_visible = True
        self.view_model.message_box_view_model.management_box_label = _("Editing message: ") if(mtype == "edit") else _("Replying to message: ")
        self.view_model.message_box_view_model.management_box_label_preview = message.message
        if mtype == "edit":
            self.view_model.message_box_view_model.entry_text = message.message

    def _set_message_for_deletion(self, child, message_id):
        self.view_model.delete_message(message_id)

    def _message_sent_event(self, child, message, files):
        self.view_model.send_message(message, files)

    def _scroll_to_bottom(self):
        vadjust = self.message_list.get_vadjustment()
        if vadjust:
            vadjust.set_value(vadjust.get_upper() - vadjust.get_page_size())
            return False

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
