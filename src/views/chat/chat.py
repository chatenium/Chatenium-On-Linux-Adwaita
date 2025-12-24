from gi.repository import Adw
from gi.repository import Gtk
from backend.chat.chats_handler import ChatsHandler
from backend.session_manager import SessionManager
from .dm import DmView
from .async_image import AsyncImage
from backend.websocket import WebSocket
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        print(SessionManager.instance().currentSession)

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
        chats = await ChatsHandler.instance().getChats()
        print(chats)
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
