from gi.repository import Adw, Gtk, Gdk, GLib
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

    def _scroll_to_bottom(self):
        print("Scrolling to bottom")
        vadjust = self.message_list.get_vadjustment()
        if vadjust:
            vadjust.set_value(vadjust.get_upper() - vadjust.get_page_size())
            return False

    def _refresh_message_list(self, messages):
        def _do():
            print("Refreshing")
            self.message_list_box.remove_all()

            print("Looping")

            for message in messages:
                row = Gtk.ListBoxRow()
                box = Gtk.Box()
                label = Gtk.Label(label=str(message.message or ""))
                label.set_wrap(True)

                box.append(label)

                if message.author == SessionManager.instance().currentSession[1].userid:
                    box.set_halign(Gtk.Align.END)

                row.set_child(box)
                self.message_list_box.append(row)

            print("Looping ok")

            self.message_list_holder.set_visible_child(self.message_list)

            GLib.timeout_add(1000, self._scroll_to_bottom)

        GLib.idle_add(_do)


    async def _load_messages(self):
        messages = await DmHandler.instance().get_messages(self.chatdata.chatid)
        self._refresh_message_list(messages)

    @Gtk.Template.Callback()
    def on_entry_activate(self, entry):
        threading.Thread(
            target=asyncio.run(self._do_send_message(entry.get_text())),
            daemon=True
        ).start()
        entry.set_text("")

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
