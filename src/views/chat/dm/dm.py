from gi.repository import Adw, Gtk, Gdk
from backend.chat.dm.dm_handler import DmHandler, Attachment
from backend.session_manager import SessionManager
import os
import threading
import asyncio
import time

@Gtk.Template(resource_path='/hu/chatenium/chtnoladw/views/chat/dm/dm.ui')
class DmView(Gtk.Box):
    __gtype_name__ = 'DmView'

    message_list_holder = Gtk.Template.Child()
    message_list = Gtk.Template.Child()
    message_list_loader = Gtk.Template.Child()
    message_list_box = Gtk.Template.Child()

    def __init__(self, chat, **kwargs):
        super().__init__(**kwargs)
        self.message_list_holder.set_visible_child(self.message_list_loader)
        self.message_list_loader.start()
        self.chatdata = chat
        self.add_styles()
        DmHandler.instance().subscribe(self._refresh_message_list)
        threading.Thread(
            target=lambda: asyncio.run(DmHandler.instance().join_chat(chat.chatid)),
            daemon=True
        ).start()
        threading.Thread(
            target=lambda: asyncio.run(self._load_messages()),
            daemon=True
        ).start()

    def _refresh_message_list(self, messages):
        print("Refreshing")
        self.message_list_box.remove_all()

        for message in messages:
            row = Gtk.Box()
            row.append(Gtk.Label(label=message.message))

            if message.author == SessionManager.instance().currentSession[1].userid:
                row.set_halign(Gtk.Align.END)

            self.message_list_box.append(row)
        self.message_list_holder.set_visible_child(self.message_list)

        self.message_list.set_opacity(0)
        time.sleep(.1)
        scrolled = self.message_list
        vadjust = scrolled.get_vadjustment()
        vadjust.set_value(vadjust.get_upper() - vadjust.get_page_size())
        self.message_list.set_opacity(1)

    async def _load_messages(self):
        messages = await DmHandler.instance().get_messages(self.chatdata.chatid)
        self._refresh_message_list(messages)

    @Gtk.Template.Callback()
    def on_entry_activate(self, entry):
        threading.Thread(
            target=asyncio.run(self._do_send_message(entry.get_text())),
            daemon=True
        ).start()

    async def _do_send_message(self, message):
        try:
            result = await DmHandler.instance().send_message(self.chatdata.chatid, message)
        except Exception as e:
            print(e)

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
