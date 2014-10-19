from gi.repository import Gtk

class AboutDialog(Gtk.AboutDialog):
	""" Extends basic AboutDialog to display needed values """

	def __init__(self, parent):
		super(AboutDialog, self).__init__(parent)

		self.set_program_name("Librethon")
		self.set_version("1.1")
		self.set_website("https://github.com/Pyr0x1/Librethon")
		self.set_copyright("developed by\nLoris \"Pyrox\" Gabriele")
		self.set_comments("A simple electronic academic transcript written in Python and GTK+")
		self.set_license("The MIT License (MIT)\n\nCopyright (c) 2014 Loris \"Pyrox\" Gabriele\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the \"Software\"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in\nall copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\nTHE SOFTWARE.")