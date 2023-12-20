import sublime
import sublime_plugin
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
import re

file_saved_on_disk = False

# conversion from sublime encoding to python encoding
# taken from https://github.com/rosshemsley/SublimeClangFormat/
subl_to_python_encoding = {
   "UTF-8" : "utf-8",
   "UTF-8 with BOM" : "utf-8-sig",
   "UTF-16 LE" : "utf-16-le",
   "UTF-16 LE with BOM" : "utf-16",
   "UTF-16 BE" : "utf-16-be",
   "UTF-16 BE with BOM" : "utf-16",
   "Western (Windows 1252)" : "cp1252",
   "Western (ISO 8859-1)" : "iso8859-1",
   "Western (ISO 8859-3)" : "iso8859-3",
   "Western (ISO 8859-15)" : "iso8859-15",
   "Western (Mac Roman)" : "mac-roman",
   "DOS (CP 437)" : "cp437",
   "Arabic (Windows 1256)" : "cp1256",
   "Arabic (ISO 8859-6)" : "iso8859-6",
   "Baltic (Windows 1257)" : "cp1257",
   "Baltic (ISO 8859-4)" : "iso8859-4",
   "Celtic (ISO 8859-14)" : "iso8859-14",
   "Central European (Windows 1250)" : "cp1250",
   "Central European (ISO 8859-2)" : "iso8859-2",
   "Cyrillic (Windows 1251)" : "cp1251",
   "Cyrillic (Windows 866)" : "cp866",
   "Cyrillic (ISO 8859-5)" : "iso8859-5",
   "Cyrillic (KOI8-R)" : "koi8-r",
   "Cyrillic (KOI8-U)" : "koi8-u",
   "Estonian (ISO 8859-13)" : "iso8859-13",
   "Greek (Windows 1253)" : "cp1253",
   "Greek (ISO 8859-7)" : "iso8859-7",
   "Hebrew (Windows 1255)" : "cp1255",
   "Hebrew (ISO 8859-8)" : "iso8859-8",
   "Nordic (ISO 8859-10)" : "iso8859-10",
   "Romanian (ISO 8859-16)" : "iso8859-16",
   "Turkish (Windows 1254)" : "cp1254",
   "Turkish (ISO 8859-9)" : "iso8859-9",
   "Vietnamese (Windows 1258)" :  "cp1258",
   "Hexadecimal" : None,
   "Undefined" : None
}

def binary_exists(binary):
	if shutil.which(binary) == None:
		sublime.error_message("Clang binary is not found. Check if you have clang-format installed")
		return False
	return True

def file_language_supported(supported_languages):
	view = sublime.active_window().active_view()
	filename_language_syntax_path = view.settings().get('syntax')
	filename_language, extension = os.path.splitext(os.path.basename(filename_language_syntax_path))
	if len(supported_languages):
		for language in supported_languages:
			if language == filename_language:
				return True
	return False

def get_python_encoding():
	view = sublime.active_window().active_view()
	subl_encoding = view.encoding()
	py_encoding = subl_to_python_encoding[subl_encoding]
	if py_encoding == None:
		py_encoding = 'utf-8'
	return py_encoding

def execute_command(command):
	view = sublime.active_window().active_view()

	py_encoding = get_python_encoding()
	buffer = view.substr(sublime.Region(0, view.size()))
	buffer_encoded = buffer.encode(py_encoding)

	proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
	output, error = proc.communicate(buffer_encoded)
	if error:
		command_str = ' '.join(str(element) for element in command)
		sublime.error_message("COMMAND FAILED: " + command_str)

	output = output.decode(py_encoding)
	return output

def formating_needed(binary, config_file_path, filename):
	command = [binary, '--output-replacements-xml', filename]
	if config_file_path == None:
		command.append('-style')
		command.append('file')
	else:
		command.append('-style')
		command.append('file:' + config_file_path)

	command_xml_output = execute_command(command)

	formating_needed = parse_xml(command_xml_output)
	return formating_needed

def parse_xml(buffer):
	tree = ET.ElementTree(ET.fromstring(buffer))
	root = tree.getroot()
	if len(list(root)) > 0:
		return True
	return False

def clang_version_13_or_lower(binary):
	command = [binary, '--version']
	command_output = execute_command(command)
	clang_version_14_or_newer = re.search(r'[1-9][456789]+\.[0-9]+\.[0-9]+', command_output)
	if not clang_version_14_or_newer:
		return True
	return False

def run_clang_format(view):
	global file_saved_on_disk
	if not file_saved_on_disk:
		file_saved_on_disk = True
		view.run_command('save')
	user_settings = sublime.load_settings('clang_format.sublime-settings')
	format_on_save = user_settings.get('format_on_save', 'false')
	if format_on_save:
		file_saved_on_disk = False
		view.run_command("clang_format")

# Triggered when ST clang_format command is executed
class ClangFormatCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		user_settings = sublime.load_settings('clang_format.sublime-settings')
		binary = user_settings.get('binary', 'clang-format')
		supported_languages = user_settings.get('supported_languages', [])
		config_file_path = user_settings.get('config_file_path', None)
		filename = self.view.file_name()

		if not file_language_supported(supported_languages):
			return

		if not binary_exists(binary):
			return

		if not formating_needed(binary, config_file_path, filename):
			return

		command = [binary, '-style']
		if config_file_path == None or clang_version_13_or_lower(binary):
			command.append('file')
			command.append(filename)
		else:
			command.append('file:' + config_file_path)
			command.append(filename)

		command_output = execute_command(command)

		self.view.replace(edit, sublime.Region(0, self.view.size()), command_output)

class ClangFormatEventListener(sublime_plugin.EventListener):
	def on_pre_save(self, view):
		run_clang_format(view)