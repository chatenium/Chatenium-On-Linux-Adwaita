from gi.repository import Gtk, Adw, GObject
from pathlib import Path
from typing import List
from .message_box_dialog import MessageBoxDialog
from .message_box_model import MessageBoxViewModel

@Gtk.Template(resource_path='/hu/chatenium/chtnoladw/views/chat/elements/message_box/message_box.ui')
class MessageBox(Gtk.Box):
    __gtype_name__ = 'MessageBox'
    __gsignals__ = {
        "message-sent": (GObject.SIGNAL_RUN_FIRST, None, (str,GObject.TYPE_PYOBJECT))
    }

    entry = Gtk.Template.Child()
    message_management_box = Gtk.Template.Child()
    message_management_msg_preview = Gtk.Template.Child()
    message_management_type_label = Gtk.Template.Child()

    def __init__(self, view_model: MessageBoxViewModel, **kwargs):
        super().__init__(**kwargs)
        self.view_model = view_model
        self.message_management_box.bind_property("visible", self.view_model, "management_box_visible", GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL)
        self.message_management_type_label.bind_property("label", self.view_model, "management_box_label", GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL)
        self.message_management_msg_preview.bind_property("label", self.view_model, "management_box_label_preview", GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL)
        self.entry.bind_property("text", self.view_model, "entry_text", GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL)

    @Gtk.Template.Callback()
    def on_entry_activate(self, entry):
        if self.entry.get_text().strip() != "":
            self.emit("message-sent", self.entry.get_text(), [])
            entry.set_text("")

    @Gtk.Template.Callback()
    def on_upload_clicked(self, button):
        parent_window = self.get_root()

        dialog = Gtk.FileDialog.new()
        dialog.set_title("Select files")
        dialog.set_modal(True)

        # Show asynchronously and pass the callback
        dialog.open_multiple(
            parent=parent_window,
            callback=self._on_files_selected,
            user_data=None  # optional
        )

    # Callback must have 3 parameters
    def _on_files_selected(self, dialog, result, user_data):
        try:
            files = dialog.open_multiple_finish(result)
        except Exception as e:
            print("Failed to finish FileDialog:", e)
            return

        if not files:
            print("No files selected")
            return

        converted_files: List[Path] = []

        for f in files:
            converted_files.append(Path(f.get_path()))

        main_window = self.get_root().get_root()
        mbdialog = MessageBoxDialog(converted_files)
        mbdialog.connect("message-sent", self._handle_dialog_send)
        mbdialog.present(main_window)

    @Gtk.Template.Callback()
    def cancel_message_management(self, button):
        self.view_model.management_box_visible = False
        self.view_model.management_type = None
        self.view_model.entry_text = ""

    def _handle_dialog_send(self, child, message, files):
        self.emit("message-sent", message, files)
        self.view_model.management_box_visible = False
        self.view_model.management_type = None

