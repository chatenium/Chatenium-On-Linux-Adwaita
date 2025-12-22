from gi.repository import Adw
from gi.repository import Gtk
from .chat_row import ChatRow
from backend.chat.chats_handler import ChatsHandler
from backend.session_manager import SessionManager
import threading
import asyncio

@Gtk.Template(resource_path='/hu/chatenium/chtnoladw/views/chat/chat.ui')
class ChatView(Gtk.Box):
    __gtype_name__ = 'ChatView'

    chat_list = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        print(SessionManager.instance().currentSession)

        threading.Thread(
            target=lambda: asyncio.run(self._load_chats()),
            daemon=True
        ).start()

    async def _load_chats(self):
        chats = await ChatsHandler.instance().getChats()
        print(chats)
        self.chat_list.append(ChatRow())
