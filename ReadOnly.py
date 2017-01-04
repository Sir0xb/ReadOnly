import sublime
import sublime_plugin

conf = None
plugin_key_name = "readonly_status"

def plugin_loaded():
	global conf
	conf = sublime.load_settings("ReadOnly.sublime-settings")

class MyEventListener(sublime_plugin.EventListener):
	def on_load(self, view):
		if conf.get("auto_readonly"):
			view.run_command("set_readonly")
			view.set_status(plugin_key_name, "readonly")
		else:
			view.run_command("set_writable")
			view.set_status(plugin_key_name, "writable")

	def on_activated(self, view):
		view.set_status(plugin_key_name, view.is_read_only() and "readonly" or "writable")

	def on_deactivated(self, view):
		if conf.get("deactivated_lock"):
			view.set_read_only(True)

class SetReadonlyCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.set_read_only(True)
		self.view.set_status(plugin_key_name, "readonly")

class SetWritableCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.set_read_only(False)
		self.view.set_status(plugin_key_name, "writable")

class ToggleAutoReadonlyCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if conf.get("auto_readonly"):
			conf.set("auto_readonly", False)
		else:
			conf.set("auto_readonly", True)
