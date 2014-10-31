#!/usr/bin/python

from gi.repository import Gtk, GLib
from os.path import expanduser
import sys
import signal
import os
from AddDialog import *
from AboutDialog import *

class MainWindow(Gtk.Window):
	""" Main program window, extended by GtkWindow widget """

	def __init__(self, data_file, settings_file, icon_file):
		super(MainWindow, self).__init__(title="Librethon")

		# Store paths for data and settings
		self.data_file = data_file
		self.settings_file = settings_file
		self.icon_file = icon_file

		# Load settings
		self.settings = {}
		self.__read_settings_from_file(self.settings_file)

		# Window properties
		if "width" in self.settings and "height" in self.settings:
			self.set_default_size(self.settings["width"], self.settings["height"])
		self.set_position(Gtk.WindowPosition.CENTER)
		self.connect("delete-event", self.__main_window_quit)
		self.connect("check-resize", self.__update_window_size)

		# Load icon
		#self.set_icon_from_file(self.icon_file)
		self.set_default_icon_from_file(self.icon_file)

		# Vertical box to store elements
		self.vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 8)
		self.add(self.vbox)

		# Create menu
		self.menu_bar = Gtk.MenuBar.new()
		self.file_menu = Gtk.Menu.new()
		self.help_menu = Gtk.Menu.new()

		self.file_menu_label = Gtk.MenuItem.new_with_label ("File");
		self.exit_menu_label = Gtk.MenuItem.new_with_label ("Exit");
		self.help_menu_label = Gtk.MenuItem.new_with_label ("Help");
		self.info_menu_label = Gtk.MenuItem.new_with_label ("About");

		self.file_menu_label.set_submenu(self.file_menu)
		self.file_menu.append(self.exit_menu_label)
		self.menu_bar.append(self.file_menu_label)
		self.exit_menu_label.connect("activate", self.__main_window_quit)

		self.help_menu_label.set_submenu(self.help_menu)
		self.help_menu.append(self.info_menu_label)
		self.menu_bar.append(self.help_menu_label)
		self.info_menu_label.connect("activate", self.__on_about_menu_clicked)

		self.vbox.pack_start(self.menu_bar, False, False, 3)

		# Scrolled window to host marks
		self.scroll_window = Gtk.ScrolledWindow.new(None, None)
		self.vbox.pack_start(self.scroll_window, True, True, 0)

		# Model storing data
		self.list_store = Gtk.ListStore(str, int, int, str)

		self.__read_data_from_file(self.data_file)
		
		# View to display data from model
		self.view = Gtk.TreeView(self.list_store)

		self.renderer = Gtk.CellRendererText()
		self.column = Gtk.TreeViewColumn("Name", self.renderer, text=0)
		self.column.set_sort_column_id(0)
		self.view.append_column(self.column)

		self.renderer = Gtk.CellRendererText()
		self.column = Gtk.TreeViewColumn("Credits", self.renderer, text=1)
		self.column.set_sort_column_id(1)
		self.view.append_column(self.column)

		self.renderer = Gtk.CellRendererText()
		self.column = Gtk.TreeViewColumn("Vote", self.renderer, text=2)
		self.column.set_sort_column_id(2)
		self.view.append_column(self.column)

		self.renderer = Gtk.CellRendererText()
		self.column = Gtk.TreeViewColumn("Date", self.renderer, text=3)
		self.column.set_sort_column_id(3)
		self.view.append_column(self.column)

		self.scroll_window.add(self.view)

		# Horizontal box to place buttons
		self.hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 8)
		self.vbox.pack_start(self.hbox, False, True, 8)

		# Button to add new mark
		self.add_button = Gtk.Button(label="Add")
		self.hbox.pack_start(self.add_button, True, False, 3)
		self.add_button.connect("clicked", self.__on_add_button_clicked)

		# Button to edit an existing mark
		self.add_button = Gtk.Button(label="Edit")
		self.hbox.pack_start(self.add_button, True, False, 3)
		self.add_button.connect("clicked", self.__on_edit_button_clicked)

		# Button to remove mark
		self.remove_button = Gtk.Button(label="Remove")
		self.hbox.pack_start(self.remove_button, True, False, 3)
		self.remove_button.connect("clicked", self.__on_remove_button_clicked)

		# Label to display average
		self.avg_label = Gtk.Label()
		self.vbox.pack_start(self.avg_label, False, False, 0)

		# Label to display graduation mark
		self.grad_label = Gtk.Label()
		self.vbox.pack_start(self.grad_label, False, False, 10)

		# Write values in labels
		if len(self.list_store) > 0:
			self.__update_labels()

		# Handles anomalous closing of the program
		# signal.signal(signal.SIGINT, self.__cleanup_quit)
		# signal.signal(signal.SIGINT, signal.SIG_DFL)
		self.__init_signal()

	def __read_data_from_file(self, filename):
		""" To be called only in the class constructor """

		try:
			with open(filename, "r") as textfile:
				for line in textfile:
					line_split = line.split(",")

					name = line_split[0]
					credits = int(line_split[1])
					mark = int(line_split[2])
					date = line_split[3].strip("\n")

					if name != "" and credits >= 1 and mark >= 18 and mark <= 30:
						self.list_store.append([name, credits, mark, date])
					else:
						raise Exception("Imported illegal values, please fix them (or avoid messing up with input file)")
		except IOError:
			print "First time running the program, no data file"

	def __write_data_to_file(self, filename):
		""" To be called at the end of the main Gtk loop (or when the store list is modified) """

		# If not present (first time launching), create dir in user's home
		if not os.path.exists(os.path.dirname(self.data_file)): # could use self.settings_file as well
			os.makedirs(os.path.dirname(self.data_file))

		with open(filename, "w+") as textfile:
			for row in self.list_store:
				textfile.write(row[0] + "," + str(row[1]) + "," + str(row[2]) + "," + row[3] + "\n")

	def __read_settings_from_file(self, filename):
		""" To be called only in the class constructor """
		try:
			with open(filename, "r") as textfile:
				self.settings = {}
				for line in textfile:
					line_split = line.split(":")
					line_split[0] = line_split[0].strip(" ")
					line_split[1] = line_split[1].strip(" ")
					self.settings[line_split[0]] = int(line_split[1])
		except IOError:
			print "First time running the program, no cfg file"

	def __write_settings_to_file(self, filename):
		""" To be called at the end of the main Gtk loop (or when the settings are modified) """

		# If not present (first time launching), create dir in user's home
		if not os.path.exists(os.path.dirname(self.data_file)): # could use self.settings_file as well
			os.makedirs(os.path.dirname(self.data_file))

		with open(filename, "w+") as textfile:
			for key in self.settings:
				textfile.write(key + " : " + str(self.settings[key]) + "\n")

	def __main_window_quit(self, window, event=None):
		self.__write_settings_to_file(self.settings_file)
		self.__write_data_to_file(self.data_file)
		Gtk.main_quit()
		return True

	def __cleanup_quit(self):
		print "Received termination signal, aborting after saving data..."
		self.present()
		self.__main_window_quit(self)

	def __on_add_button_clicked(self, button):
		dialog = AddDialog(self)
		
		response = dialog.run()

		if response == Gtk.ResponseType.ACCEPT:
			name = dialog.get_name()
			credits = dialog.get_credits()
			mark = dialog.get_mark()
			date = dialog.get_date()

			if name != "" and credits >= 1 and mark >= 18 and mark <= 30:
				self.list_store.append([name, credits, mark, date])
				self.__write_data_to_file(self.data_file)
				self.__update_labels()

		dialog.destroy()

	def __on_edit_button_clicked(self, button):
		selection = self.view.get_selection()
		model, store_iter = selection.get_selected()

		# First check if a selection is made
		if store_iter != None:
			old_name = self.list_store[store_iter][0]
			old_credits = self.list_store[store_iter][1]
			old_mark = self.list_store[store_iter][2]
			old_date = self.list_store[store_iter][3]

			dialog = AddDialog(self, old_name, old_credits, old_mark, old_date)

			response = dialog.run()

			if response == Gtk.ResponseType.ACCEPT:
				name = dialog.get_name()
				credits = dialog.get_credits()
				mark = dialog.get_mark()
				date = dialog.get_date()

				if name != "" and credits >= 1 and mark >= 18 and mark <= 30:
					self.list_store.set_value(store_iter, 0, name)
					self.list_store.set_value(store_iter, 1, credits)
					self.list_store.set_value(store_iter, 2, mark)
					self.list_store.set_value(store_iter, 3, date)

					self.__write_data_to_file(self.data_file)
					self.__update_labels()

			dialog.destroy()

	def __on_remove_button_clicked(self, button):
		selection = self.view.get_selection()
		model, store_iter = selection.get_selected()

		# First check if a selection is made
		if store_iter != None:
			self.list_store.remove(store_iter)
			self.__write_data_to_file(self.data_file)
			self.__update_labels()

	def __on_about_menu_clicked(self, button):
		about_dialog = AboutDialog(self)
		about_dialog.run()
		about_dialog.destroy()

	def __calc_avg(self):
		vote_sum = 0
		tot_cred = 0

		for row in self.list_store:
			vote_sum += row[1] * row[2]
			tot_cred += row[1]

		return float(vote_sum) / tot_cred

	def __calc_grad(self, avg):
		return avg * 110 / 30

	def __calc_purified_avg(self, num_cred):
		tot_cred = 0

		for row in self.list_store:
			tot_cred += row[1]

		if num_cred < tot_cred:
			cred_list = []

			# Create a list where each element is the value of a credit
			for row in self.list_store:
				for elem in range(row[2]):
					cred_list.append(row[1])

			cred_list.sort() # Sorts list so worst credits are first

			for elem in range(num_cred): # Removes first n credits (worst ones)
				cred_list.pop(0)

			# Compute purified average
			vote_sum = 0
			for elem in cred_list:
				vote_sum += elem

			tot_cred -= num_cred

			return float(vote_sum) / tot_cred

		else:
			return 0 # Not enough credits to compute purified average

	def __update_labels(self):
		# Calculate average to display once all data is loaded
		avg = self.__calc_avg()
		string = "Average: %.2f" % avg
		self.avg_label.set_label(string)

		# Calculate graduation mark and display it
		grad = self.__calc_grad(avg)
		string = "Graduation Mark (expected): %i" % grad
		self.grad_label.set_label(string)

	def __update_window_size(self, window):
		width, height = self.get_size()
		self.settings["width"] = width
		self.settings["height"] = height
		#self.__write_settings_to_file(self.settings_file)

	# Workaround to correctly set signal handling (thanks to stack overflow user "Ascot")
	def __init_signal(self):
	    def signal_action(signal):
	        if signal is 1:
	            # print("Caught signal SIGHUP(1)")
	            pass
	        elif signal is 2:
	            # print("Caught signal SIGINT(2)")
	            pass
	        elif signal is 15:
	            # print("Caught signal SIGTERM(15)")
	            pass
	        self.__cleanup_quit()

	    def idle_handler(*args):
	        print("Python signal handler activated.")
	        GLib.idle_add(signal_action, priority=GLib.PRIORITY_HIGH)

	    def handler(*args):
	        print("GLib signal handler activated.")
	        signal_action(args[0])

	    def install_glib_handler(sig):
	        unix_signal_add = None

	        if hasattr(GLib, "unix_signal_add"):
	            unix_signal_add = GLib.unix_signal_add
	        elif hasattr(GLib, "unix_signal_add_full"):
	            unix_signal_add = GLib.unix_signal_add_full

	        if unix_signal_add:
	            # print("Register GLib signal handler: %r" % sig)
	            unix_signal_add(GLib.PRIORITY_HIGH, sig, handler, sig)
	        else:
	            print("Can't install GLib signal handler, too old gi.")

	    SIGS = [getattr(signal, s, None) for s in "SIGINT SIGTERM SIGHUP".split()]
	    for sig in filter(None, SIGS):
	        # print("Register Python signal handler: %r" % sig)
	        signal.signal(sig, idle_handler)
	        GLib.idle_add(install_glib_handler, sig, priority=GLib.PRIORITY_HIGH)

if __name__ == "__main__":
	#home = expanduser("~")
	#win = MainWindow(home + "/.librethon/data", home + "/.librethon/cfg", "/usr/share/pixmaps/librethon.png")
	win = MainWindow("../data/data", "../data/cfg", "../data/librethon.png")
	win.show_all()
	Gtk.main()