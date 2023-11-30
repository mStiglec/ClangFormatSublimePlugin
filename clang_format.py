import sublime
import sublime_plugin
import os
import distutils.spawn
import shutil
import subprocess

# conversion from sublime encoding to python encoding
# code taken from https://github.com/rosshemsley/SublimeClangFormat/
st_encodings_trans = {
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

def file_language_is_supported(supported_languages, filename_language):
	if len(supported_languages):
		for language in supported_languages:
			if language == filename_language:
				return True
	return False

# Triggered when clang_format command is executed
class ClangFormatCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		settings_global = sublime.load_settings('clang_format.sublime-settings')

		supported_languages = settings_global.get('languages', [])
		filename_language_syntax_path = self.view.settings().get('syntax')
		filename_language, extension = os.path.splitext(os.path.basename(filename_language_syntax_path))
		if not file_language_is_supported(supported_languages, filename_language):
			return

		binary = settings_global.get('binary', 'clang-format')
		if not binary_exists(binary):
			return

		file_encoding_subl = self.view.encoding()
		file_encoding_py = st_encodings_trans[file_encoding_subl]
		if file_encoding_py == None:
			file_encoding_py = 'utf-8'

		buffer = self.view.substr(sublime.Region(0, self.view.size()))
		buffer_encoded = buffer.encode(file_encoding_py)

		# check if anything to format, if not then return

		filename_path = self.view.file_name()
		command = [binary, '-style', 'file', filename_path]

		proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		print(subprocess.list2cmdline(command))
		output, error = proc.communicate(buffer_encoded)
		if error:
			sublime.error_message("clang-format failed. Check if clang-format exists in your system")
			return

		buffer_decoded = output.decode(file_encoding_py)
		self.view.replace(edit, sublime.Region(0, self.view.size()), buffer_decoded)

class autoClangOnSave(sublime_plugin.EventListener):
	def on_pre_save_async(self, view):
		syntax_path = view.settings().get("syntax")
		filename, _extension = os.path.splitext(os.path.basename(syntax_path))
		settings_global = sublime.load_settings('clang_format.sublime-settings')
		supported_languages = settings_global.get('languages', [])
		if not file_language_is_supported(supported_languages, filename):
			return
		view.run_command("clang_format")
