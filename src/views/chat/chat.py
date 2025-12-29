from gi.repository import Adw, Gtk, GLib
from backend.chat.chats_handler import ChatsHandler
from backend.session_manager import SessionManager
from .dm import DmView
from .async_image import AsyncImage
from backend.websocket import WebSocket
from backend.http import GenericErrorBody
import threading
import asyncio

@Gtk.Template(resource_path='/hu/chatenium/chtnoladw/views/chat/chat.ui')
class ChatView(Gtk.Box):
    __gtype_name__ = 'ChatView'

    chat_list = Gtk.Template.Child()
    chat_list_holder = Gtk.Template.Child()
    chat_list_loader = Gtk.Template.Child()
    main_content = Gtk.Template.Child()
    chat_list_scroller = Gtk.Template.Child()
    sidenav_header_bar = Gtk.Template.Child()
    start_chat_dialog = Gtk.Template.Child()
    start_new_chat_p_uname_entry = Gtk.Template.Child()
    start_new_toast_ol = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        startBtn = Gtk.Button()
        startBtn.set_icon_name("value-increase-symbolic")
        startBtn.connect("clicked", self.start_chat_dialog.present)
        self.sidenav_header_bar.pack_end(startBtn)

        threading.Thread(
            target=asyncio.run(WebSocket.instance().connect()),
            daemon=True
        ).start()

        self.chat_list_holder.set_visible_child(self.chat_list_loader)
        self.chat_list_loader.start()

        threading.Thread(
            target=lambda: asyncio.run(self._load_chats()),
            daemon=True
        ).start()

    @Gtk.Template.Callback()
    def on_chat_selected(self, listbox, item):
        chat = item.chat_data
        self.main_content.set_content(DmView(chat))

    async def _load_chats(self):
        def _do(chats):
            self.chat_list.remove_all()
            self.chat_list_holder.set_visible_child(self.chat_list_scroller)
            for chat in chats:
                row = Adw.ActionRow()

                name = chat.displayName
                if chat.displayName == "":
                    name = "@"+chat.username

                avatar_img = AsyncImage(chat.pfp, placeholder_icon="avatar-default-symbolic", height=35, width=35)

                row.add_prefix(avatar_img)
                row.set_title(name)
                row.chat_data = chat
                self.chat_list.append(row)

        chats = await ChatsHandler.instance().getChats()
        GLib.idle_add(_do, chats)

    @Gtk.Template.Callback()
    def on_start_chat(self, button):
        threading.Thread(
            target=lambda: asyncio.run(self._do_start_chat(self.start_new_chat_p_uname_entry.get_text())),
            daemon=True
        ).start()

    async def _do_start_chat(self, pUsername):
        try:
            await ChatsHandler.instance().startNew(pUsername)
            await self._load_chats()

        except Exception as e:
            _("addUserUnk")
            _("noStartChatWithSelf")
            _("chatAlreadyExists")
            toast = Adw.Toast.new(_(f"{e}"))
            self.start_new_toast_ol.add_toast(toast)


