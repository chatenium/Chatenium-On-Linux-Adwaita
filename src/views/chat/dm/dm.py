from gi.repository import Adw, Gtk, Gdk
from backend.chat.dm.dm_handler import DmHandler, Attachment
from backend.session_manager import SessionManager
import os
import threading
import asyncio

@Gtk.Template(resource_path='/hu/chatenium/chtnoladw/views/chat/dm/dm.ui')
class DmView(Gtk.Box):
    __gtype_name__ = 'DmView'

    message_list_holder = Gtk.Template.Child()
    message_list = Gtk.Template.Child()
    message_list_loader = Gtk.Template.Child()

    def __init__(self, chat, **kwargs):
        super().__init__(**kwargs)
        self.message_list_holder.set_visible_child(self.message_list_loader)
        self.message_list_loader.start()
        self.chatdata = chat
        self.add_styles()
        threading.Thread(
            target=lambda: asyncio.run(self._load_messages()),
            daemon=True
        ).start()

    async def _load_messages(self):
        messages = await DmHandler.instance().get_messages(self.chatdata.chatid)

        for message in messages:
            row = Gtk.Box()
            row.append(Gtk.Label(label=message.message))

            if message.author == SessionManager.instance().currentSession[1].userid:
                row.set_halign(Gtk.Align.END)

            self.message_list.append(row)

        self.message_list_holder.set_visible_child(self.message_list)

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
