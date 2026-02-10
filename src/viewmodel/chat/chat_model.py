from gi.repository import Gtk, GObject, Gio, GLib
from backend.chat.chats_handler import Chat, ChatsHandler, LatestMessage
import threading
import asyncio

class LatestMessageAdapter(GObject.Object):
    msgid = GObject.Property(type=str)
    message = GObject.Property(type=str)
    is_author = GObject.Property(type=bool, default=False)

    def __init__(self, latest_message: LatestMessage):
        super().__init__()
        self.msgid = latest_message.msgid
        self.messageg = latest_message.message
        self.is_author = latest_message.isAuthor

class ChatAdapter(GObject.Object):
    userid = GObject.Property(type=str)
    chatid = GObject.Property(type=str)
    username = GObject.Property(type=str)
    display_name = GObject.Property(type=str)
    pfp = GObject.Property(type=str)
    status = GObject.Property(type=int)
    pinned_messages = GObject.Property(type=str)
    type = GObject.Property(type=str)
    muted = GObject.Property(type=bool, default=False)
    latest_message = GObject.Property(type=GObject.Object)
    notifications = GObject.Property(type=int, default=0)

    def __init__(self, chat: Chat):
        super().__init__()
        self.userid = chat.userid
        self.chatid = chat.chatid
        self.username = chat.username
        self.display_name = chat.displayName
        self.pfp = chat.pfp
        self.status = chat.status
        self.pinned_messages = chat.pinnedMessages
        self.type = chat.type
        self.muted = chat.muted
        self.latest_message = LatestMessageAdapter(chat.latestMessage)
        self.notifications = chat.notifications or 0

class ChatViewModel(GObject.Object):
    chats = Gio.ListStore(item_type=ChatAdapter)

    async def load_chats(self):
        def _update_ui(api_chats):
            for chat in api_chats:
                self.chats.append(ChatAdapter(chat))
            print("Chat import to ViewModel finished successfully.")

        api_chats = await ChatsHandler.instance().getChats()
        GLib.idle_add(_update_ui, api_chats)
