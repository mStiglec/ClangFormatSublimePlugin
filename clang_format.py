import sublime
import sublime_plugin
import os
import distutils.spawn
import shutil
import subprocess

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
		print("mjau")
		settings_global = sublime.load_settings('clang_format.sublime-settings')

		supported_languages = settings_global.get('languages', [])
		filename_language_syntax_path = self.view.settings().get('syntax')
		filename_language, extension = os.path.splitext(os.path.basename(filename_language_syntax_path))
		if not file_language_is_supported(supported_languages, filename_language):
			return

		binary = settings_global.get('binary', 'clang-format')
		if not binary_exists(binary):
			return

		filename_path = self.view.file_name()
		command = [binary, '-style', 'file', '-i', filename_path]

		buf = self.view.substr(sublime.Region(0, self.view.size()))

		proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		output, error = proc.communicate(buf.encode('utf-8'))
		if error:
			sublime.error_message("clang-format failed. Check if clang-format exists in your system")
			return

		self.view.replace(edit, sublime.Region(0, self.view.size()), output.decode('utf-8'))
