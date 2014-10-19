from gi.repository import Gtk

class AddDialog(Gtk.Dialog):
	""" Extends basic Dialog to display needed widgets """

	def __init__(self, parent, name=None, credits=None, mark=None, date=None):
		super(AddDialog, self).__init__("Add Mark", parent, 0, ("Cancel", Gtk.ResponseType.REJECT, "Ok", Gtk.ResponseType.ACCEPT))

		self.set_modal(True)
		self.set_destroy_with_parent (True)
		vbox = self.get_content_area()

		grid = Gtk.Grid.new()
		grid.set_row_spacing(10);
		grid.set_column_spacing(10);

		vbox.add(grid)

		label = Gtk.Label.new("Name: ")
		grid.attach(label, 0, 0, 1, 1)

		self.entry_name = Gtk.Entry.new()
		grid.attach(self.entry_name, 1, 0, 1, 1)
		if name is not None:
			self.entry_name.set_text(name)

		label = Gtk.Label.new("Credits: ")
		grid.attach(label, 0, 1, 1, 1)

		self.spin_button_credits = Gtk.SpinButton.new_with_range(1, 30, 1)
		grid.attach(self.spin_button_credits, 1, 1, 1, 1)
		if credits is not None:
			self.spin_button_credits.set_value(int(credits))

		label = Gtk.Label.new("Vote: ")
		grid.attach(label, 0, 2, 1, 1)

		self.spin_button_mark = Gtk.SpinButton.new_with_range(18, 30, 1)
		grid.attach(self.spin_button_mark, 1, 2, 1, 1)
		if mark is not None:
			self.spin_button_mark.set_value(int(mark))

		label = Gtk.Label.new("Date: ")
		grid.attach(label, 0, 3, 1, 1)

		self.calendar = Gtk.Calendar.new()
		grid.attach(self.calendar, 1, 3, 1, 1)
		if date is not None:
			token = date.split("/")
			self.calendar.select_month(int(token[1]) - 1, int(token[0]))
			self.calendar.select_day(int(token[2]))

		hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 8)
		vbox.pack_start(hbox, True, False, 3)

		hseparator = Gtk.Separator.new(Gtk.Orientation.HORIZONTAL)
		vbox.pack_start(hseparator, True, False, 3)

		self.show_all()

	def get_name(self):
		return self.entry_name.get_text()

	def get_credits(self):
		return int(self.spin_button_credits.get_value())

	def get_mark(self):
		return int(self.spin_button_mark.get_value())

	def get_date(self):
		date = self.calendar.get_date()

		return str(date[0]) + "/" + str(date[1]) + "/" + str(date[2])