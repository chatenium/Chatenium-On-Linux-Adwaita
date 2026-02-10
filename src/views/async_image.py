import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GdkPixbuf, GLib, Gdk
import threading
import urllib.request
import requests

class AsyncImage(Gtk.Picture):
    def __init__(self, url):
        super().__init__()
        self.set_css_classes(["rounded"])
        threading.Thread(target=self._download, args=(url,), daemon=True).start()

    def _download(self, url):
        try:
            response = requests.get(url)
            data = response.content
            bytes_ = GLib.Bytes.new(data)
            texture = Gdk.Texture.new_from_bytes(bytes_)
            self.set_paintable(texture)

        except Exception as e:
            print("AsyncImage download error:", e)
