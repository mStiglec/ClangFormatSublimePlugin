## SublimeClangFormatPlugin
[Clang-format](https://clang.llvm.org/docs/ClangFormatStyleOptions.html) plugin for Sublime Text 3.  
Option *-style=file* is used for formatting. With this option user can define and use his own configuration file.

## Install
There are two ways to install plugin:
  1. Place this repository inside:
      - *<path_to_sublime_text>/Packages/*.
  2. Using [Package Control](https://packagecontrol.io/installation). Plugin will be stored inside:
      - *<path_to_sublime_text>/Installed Packages/*

First option is recommended.

## Prerequisites
Clang-format must be installed:
   -  Linux: *sudo apt-get install clang-format*
   -  Windows: [last release](https://github.com/llvm/llvm-project/releases)

## Settings
Default settings can be found inside:
  - *<path_to_sublime_text>/Packages/ClangFormatSublimePlugin/clang_format.sublime-settings*.

User settings can be found inside:
  - *<path_to_sublime_text>/Packages/User/clang_format.sublime-settings.*

Both settings can be accessed through sublime Main Menu:
  - *Preferences --> Package Settings --> ClangFormatSublimePlugin*.

Four user options are used for plugin configuration:
| Option | Description |
|--------|-------------|
| binary | Path to clang-format executable. |
| path_to_config | Path to .clang-format configuration file. <br> This option will take effect only if used clang-format version is >=14, otherwise clang-format file must be put inside project directory (or any parent directory) <br> You can find description on clang-format [documentation](https://clang.llvm.org/docs/ClangFormatStyleOptions.html#configuring-style-with-clang-format) |
| format_on_save | If this option is set to *true* file will be formatted on each save |
| supported_languages | Formatting will be done only for languages set in this option |

## Compatibility
Plugin is tested on Ubuntu Linux 22.04, Ubuntu Linux 20.04 and Windows 10.  
Plugin should support all clang-format versions.
