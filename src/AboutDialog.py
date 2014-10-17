from gi.repository import Gtk

class AboutDialog(Gtk.AboutDialog):
	""" Extends basic AboutDialog to display needed values """

	def __init__(self, parent):
		super(AboutDialog, self).__init__(parent)

		self.set_program_name("Librethon")
		self.set_version("1.0")
		self.set_website("boh")
		self.set_website("boh")
		self.set_copyright("developed by\nLoris \"Pyrox\" Gabriele")
		self.set_comments("A simple electronic academic transcript written in Python and GTK+")