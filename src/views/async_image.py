import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GdkPixbuf, GLib, Gdk
import threading
import urllib.request
import cairo
import math

class AsyncImage(Gtk.Picture):
    def __init__(self, url, width=None, height=None, radius=20):
        super().__init__()
        self.width = width
        self.height = height
        self.radius = radius

        if width and height:
            self.set_size_request(width, height)

        # Start download in a thread
        threading.Thread(target=self._download, args=(url,), daemon=True).start()

    def _download(self, url):
        try:
            data = urllib.request.urlopen(url).read()
            loader = GdkPixbuf.PixbufLoader.new()
            loader.write(data)
            loader.close()
            pixbuf = loader.get_pixbuf()
            if not pixbuf:
                return

            # Scale to fixed size
            if not self.width and not self.height:
                width = 300
                height = pixbuf.get_height() / (pixbuf.get_width() / width)
                self.set_size_request(width, height)

            scaled_pixbuf = pixbuf.scale_simple(self.width or pixbuf.get_width(), self.height or pixbuf.get_height(), GdkPixbuf.InterpType.BILINEAR)

            # Apply rounded corners
            rounded_pixbuf = self._pixbuf_to_rounded_rect(scaled_pixbuf, self.radius)

            # Update picture on main thread
            GLib.idle_add(lambda: self.set_pixbuf(rounded_pixbuf))

        except Exception as e:
            print("AsyncImage download error:", e)

    def _pixbuf_to_rounded_rect(self, pixbuf, radius):
        w, h = pixbuf.get_width(), pixbuf.get_height()
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        cr = cairo.Context(surface)

        # Draw rounded rectangle path
        cr.new_path()
        cr.arc(radius, radius, radius, math.pi, math.pi*1.5)
        cr.arc(w - radius, radius, radius, math.pi*1.5, 0)
        cr.arc(w - radius, h - radius, radius, 0, math.pi*0.5)
        cr.arc(radius, h - radius, radius, math.pi*0.5, math.pi)
        cr.close_path()
        cr.clip()

        # Draw pixbuf inside the clipped path
        Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
        cr.paint()
        surface.flush()

        # Convert Cairo surface back to GdkPixbuf
        rounded_pixbuf = Gdk.pixbuf_get_from_surface(surface, 0, 0, w, h)
        return rounded_pixbuf

