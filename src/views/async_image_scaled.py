from gi.repository import Adw, Gtk
from .async_image import AsyncImage

class AsyncImageScaled(Gtk.Box):
    def __init__(self, url, height=35, width=35):
        super().__init__()
        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)
        self.set_size_request(width, height)
        self.set_hexpand(False)
        self.set_vexpand(False)

        # Clamp inside box
        clamp = Adw.Clamp()
        clamp.set_maximum_size(width)
        clamp.set_size_request(width, height)

        # AsyncImage inside clamp
        picture = AsyncImage(url)
        picture.set_content_fit(Gtk.ContentFit.COVER)
        picture.set_can_shrink(True)
        picture.set_hexpand(True)
        picture.set_vexpand(True)

        clamp.set_child(picture)
        self.append(clamp)

        self.clamp = clamp
        self.picture = picture

