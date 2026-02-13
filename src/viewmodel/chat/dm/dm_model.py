from gi.repository import GObject, Gio, GLib
from backend.chat.dm.dm_handler import Message, Attachment, DmHandler, WSMessageEditPayload
from backend.types import TimeStamp
import threading
import asyncio
from typing import List
from pathlib import Path
from .message_box_model import MessageBoxViewModel

class AttachmentAdapter(GObject.Object):
    file_id = GObject.Property(type=str)
    file_name = GObject.Property(type=str)
    format = GObject.Property(type=str)
    type = GObject.Property(type=str)
    path = GObject.Property(type=str)
    height = GObject.Property(type=int)
    width = GObject.Property(type=int)
    has_thumbnail = GObject.Property(type=bool, default=False)

    def __init__(self, attachment: Attachment):
        super().__init__()
        self.file_id = attachment.fileID
        self.file_name = attachment.fileName
        self.format = attachment.format
        self.type = attachment.type
        self.path = attachment.path
        self.height = attachment.height
        self.width = attachment.width
        self.has_thumbnail = attachment.hasThumbnail

class TimeStampAdapter(GObject.Object):
    t = GObject.Property(type=int)
    i = GObject.Property(type=int)

    def __init__(self, ts: TimeStamp):
        super().__init__()
        self.t = ts.T
        self.i = ts.I

class MessageAdapter(GObject.Object):
    msgid = GObject.Property(type=str)
    author = GObject.Property(type=str)
    message = GObject.Property(type=str)
    sent_at = GObject.Property(type=GObject.TYPE_PYOBJECT)
    is_edited = GObject.Property(type=bool, default=False)
    chatid = GObject.Property(type=str)
    seen = GObject.Property(type=bool, default=False)
    reply_to = GObject.Property(type=str)
    reply_to_id = GObject.Property(type=str)
    forwarded_from = GObject.Property(type=str)
    forwarded_from_name = GObject.Property(type=str)
    files = GObject.Property(type=GObject.TYPE_PYOBJECT)

    def __init__(self, message: Message):
        super().__init__()
        self.msgid = message.msgid
        self.author = message.author
        self.message = message.message
        self.sent_at = message.sent_at
        self.is_edited = message.isEdited
        self.chatid = message.chatid
        self.seen = message.seen
        self.reply_to = message.replyTo
        self.reply_to_id = message.replyToId
        self.forwarded_from = message.forwardedFrom
        self.forwarded_from_name = message.forwardedFromName
        self.files = message.files

class DmViewModel(GObject.Object):
    messages = Gio.ListStore(item_type=MessageAdapter)

    message_box_view_model = MessageBoxViewModel()

    def __init__(self, chatdata):
        super().__init__()
        self.chatdata = chatdata

    def __del__(self):
        print(f"ViewModel cleanup")
        DmHandler.instance().unsubscribe(self._on_new_message, "add")
        DmHandler.instance().unsubscribe(self._on_edited_message, "edit")
        DmHandler.instance().unsubscribe(self._on_removed_message, "rem")

    def load_messages(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self._load_messages_async())

    async def _load_messages_async(self):
        api_messages = await DmHandler.instance().get_messages(self.chatdata.chatid)

        for message in api_messages:
            self.messages.append(MessageAdapter(message))

    async def join_chat(self):
        await DmHandler.instance().join_chat(self.chatdata.chatid)
        DmHandler.instance().subscribe(self._on_new_message, "add")
        DmHandler.instance().subscribe(self._on_edited_message, "edit")
        DmHandler.instance().subscribe(self._on_removed_message, "rem")

    def send_message(self, message: str, files: List[Path] = []):
        try:
            if self.message_box_view_model.management_type == "edit":
                print("Editing message")
                asyncio.create_task(DmHandler.instance().edit_message(self.chatdata.chatid, self.message_box_view_model.management_data.msgid, message))
            elif self.message_box_view_model.management_type == "reply":
                print("Sending message (reply)")
                asyncio.create_task(DmHandler.instance().send_message(self.chatdata.chatid, message, self.message_box_view_model.management_data.msgid, self.message_box_view_model.management_data.message, files))
            else:
                print("Sending message (noreply)")
                asyncio.create_task(DmHandler.instance().send_message(self.chatdata.chatid, message, "", "", files))

            self.message_box_view_model.management_type = ""
            self.message_box_view_model.management_box_visible = False
        except Exception as e:
            print(f"Message send failed: {e}")

    def delete_message(self, message_id: str):
        try:
            asyncio.create_task(DmHandler.instance().delete_message(self.chatdata.chatid, message_id))
        except Exception as e:
            print(f"Deleting message failed: {e}")

    def _on_new_message(self, message: Message):
        self.messages.append(MessageAdapter(message))

    def _on_edited_message(self, payload: WSMessageEditPayload):
        for i in range(self.messages.get_n_items()):
            message = self.messages.get_item(i)
            print(message)
            if message.msgid == payload.messageId:
                message.is_edited = True
                message.message = payload.message
                break

    def _on_removed_message(self, message_id: str):
        for i in range(self.messages.get_n_items()):
            message = self.messages.get_item(i)
            if message.msgid == message_id:
                print("Removed message found")
                self.messages.remove(i)
                break
