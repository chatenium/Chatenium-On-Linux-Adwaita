import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GdkPixbuf, GLib, Gdk
import threading
import urllib.request
import cairo
import math

class AsyncImage(Gtk.Image):
    def __init__(self, url, placeholder_icon="image-missing", width=None, height=None):
        super().__init__()
        self.url = url
        self.width = width or 64
        self.height = height or 64

        # Placeholder
        self.set_from_icon_name(placeholder_icon)
        self.set_size_request(self.width, self.height)

        threading.Thread(target=self._download, daemon=True).start()

    def _download(self):
        try:
            data = urllib.request.urlopen(self.url).read()
            loader = GdkPixbuf.PixbufLoader.new()
            loader.write(data)
            loader.close()
            pixbuf = loader.get_pixbuf()

            # scale
            pixbuf = pixbuf.scale_simple(self.width, self.height, GdkPixbuf.InterpType.BILINEAR)

            # make rounded
            rounded_pixbuf = self._pixbuf_to_rounded_rect(pixbuf)

            GLib.idle_add(lambda: self.set_from_pixbuf(rounded_pixbuf))
        except Exception as e:
            print("AsyncImage download error:", e)

    def _pixbuf_to_rounded_rect(self, pixbuf, radius=10):
        w, h = pixbuf.get_width(), pixbuf.get_height()
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        cr = cairo.Context(surface)

        # Draw rounded rectangle
        cr.new_path()
        cr.arc(radius, radius, radius, math.pi, math.pi*1.5)       # top-left
        cr.arc(w - radius, radius, radius, math.pi*1.5, 0)       # top-right
        cr.arc(w - radius, h - radius, radius, 0, math.pi*0.5)   # bottom-right
        cr.arc(radius, h - radius, radius, math.pi*0.5, math.pi)  # bottom-left
        cr.close_path()
        cr.clip()

        # Draw pixbuf
        Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
        cr.paint()
        surface.flush()

        return GdkPixbuf.Pixbuf.new_from_data(
            surface.get_data(),
            GdkPixbuf.Colorspace.RGB,
            True,
            8,
            w,
            h,
            surface.get_stride()
        )
