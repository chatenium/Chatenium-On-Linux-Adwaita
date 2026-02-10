from gi.repository import Gtk, Adw, GObject

@Gtk.Template(resource_path='/hu/chatenium/chtnoladw/views/chat/elements/message_box/message_box_dialog.ui')
class MessageBoxDialog(Adw.Dialog):
    __gtype_name__ = 'MessageBoxDialog'
    __gsignals__ = {
        "message-sent": (GObject.SIGNAL_RUN_FIRST, None, (str,GObject.TYPE_PYOBJECT)),
    }

    box = Gtk.Template.Child()
    upload_label = Gtk.Template.Child()
    entry = Gtk.Template.Child()

    def __init__(self, files, **kwargs):
        super().__init__(**kwargs)
        self.files = files

        self.upload_label.set_label(_(f"{len(files)} attachments selected."))

    @Gtk.Template.Callback()
    def on_entry_activate(self, entry):
        self.emit("message-sent", self.entry.get_text(), self.files)
        self.entry.set_text("")
        self.close()

    @Gtk.Template.Callback()
    def on_button_activate(self, button):
        self.emit("message-sent", "", self.files)
        self.entry.set_text("")
        self.close()
