from gi.repository import Gtk, Adw, GObject
from pathlib import Path
from typing import List
from .message_box_dialog import MessageBoxDialog

@Gtk.Template(resource_path='/hu/chatenium/chtnoladw/views/chat/elements/message_box/message_box.ui')
class MessageBox(Gtk.Box):
    __gtype_name__ = 'MessageBox'
    __gsignals__ = {
        "message-sent": (GObject.SIGNAL_RUN_FIRST, None, (str,GObject.TYPE_PYOBJECT)),
    }

    entry = Gtk.Template.Child()

    @Gtk.Template.Callback()
    def on_entry_activate(self, entry):
        if self.entry.get_text().strip() != "":
            self.emit("message-sent", self.entry.get_text())
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
            files = dialog.open_multiple_finish(result)  # MUST be called here
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

    def _handle_dialog_send(self, child, message, files):
        self.emit("message-sent", message, files)

