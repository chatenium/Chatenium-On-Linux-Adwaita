from gi.repository import GObject

class MessageBoxViewModel(GObject.Object):
    management_type = GObject.Property(type=str) # This signals the app when message management is active
    management_data = GObject.Property(type=GObject.Object) # Message
    management_box_visible = GObject.Property(type=bool, default=False)
    management_box_label = GObject.Property(type=str)
    management_box_label_preview = GObject.Property(type=str)
    entry_text = GObject.Property(type=str)
