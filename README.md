# SublimeClangFormatPlugin

## Description
This is [clang-format](https://clang.llvm.org/docs/ClangFormatStyleOptions.html) plugin for Sublime text 3.
While using sublime text for C/C++ code all plugins I tried were not intuitive and easy-to-use (at least to me).
So this is my attempt to create one.

## Install
There are two ways to install plugin:
  1. Using [Package Control](https://packagecontrol.io/installation) (plugin will be stored at <path_to_sublime_text>/Installed Packages/ folder).
  2. Place this repository inside <path_to_sublime_text>/Packages/ folder.

## Prerequisites
1. clang-format must be installed
2. clang-format configuration file must be placed inside project directory (or inside any parent directory)
   - Note: if you are using clang-format version 14 or upper you can [specify configuration file](https://clang.llvm.org/docs/ClangFormatStyleOptions.html#configuring-style-with-clang-format) path in the user settings

## Settings
Default settings can be found inside <path_to_sublime_text>/Packages/ClangFormatSublimePlugin/clang_format.sublime-settings.
User settings can be found inside <path_to_sublime_text>/Packages/User/clang_format.sublime-settings.
Both settings can be accessed through sublime Main Menu (Preferences --> Package Settings --> ClangFormatSublimePlugin).

## Compatibility
Plugin is tested on Ubuntu Linux 22.04 and 20.04.
Plugin should support all clang-format versions.
