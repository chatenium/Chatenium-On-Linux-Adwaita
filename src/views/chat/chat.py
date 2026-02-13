from gi.repository import Adw, Gtk, GLib
from backend.chat.chats_handler import ChatsHandler, Chat
from backend.session_manager import SessionManager
from .dm import DmView
from .async_image import AsyncImage
from .async_image_scaled import AsyncImageScaled
from backend.websocket import WebSocket
from backend.http import GenericErrorBody
from .chat_model import ChatViewModel, ChatAdapter
import threading
import asyncio

@Gtk.Template(resource_path='/hu/chatenium/chtnoladw/views/chat/chat.ui')
class ChatView(Gtk.Box):
    __gtype_name__ = 'ChatView'

    view_model = ChatViewModel()
    chat_list_factory = Gtk.SignalListItemFactory()

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

        self.chat_list_holder.set_visible_child(self.chat_list_loader)
        self.chat_list_loader.start()
        self.chat_list_factory.connect("setup", self.chat_list_factory_setup)
        self.chat_list_factory.connect("bind", self.chat_list_factory_bind)
        self.chat_list.set_factory(self.chat_list_factory)
        selection_model = Gtk.SingleSelection(model=self.view_model.chats)
        selection_model.connect("notify::selected", self.on_chat_selected)
        self.chat_list.set_model(selection_model)
        threading.Thread(
            target=lambda: asyncio.run(self.view_model.load_chats()),
            daemon=True
        ).start()
        self.chat_list_holder.set_visible_child(self.chat_list_scroller)

        startBtn = Gtk.Button()
        startBtn.set_icon_name("value-increase-symbolic")
        startBtn.connect("clicked", self.start_chat_dialog.present)
        self.sidenav_header_bar.pack_end(startBtn)

        asyncio.create_task(WebSocket.instance().connect())

    def on_chat_selected(self, selection, _):
        print(selection.get_selected())
        chat = self.view_model.chats[selection.get_selected()]
        self.main_content.set_content(DmView(chat))

    def chat_list_factory_setup(self, factory, list_item):
        row = Adw.ActionRow()
        list_item.row = row
        list_item.set_child(row)

    def chat_list_factory_bind(self, factory, list_item):
        chat: ChatAdapter = list_item.get_item()
        row = list_item.row
        name = chat.display_name or "@" + chat.username
        row.set_title(name)

        # Update the avatar image
        avatar_img = AsyncImageScaled(chat.pfp, height=35, width=35)
        avatar_img.set_size_request(35, 35)
        list_item.row.add_prefix(avatar_img)

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



