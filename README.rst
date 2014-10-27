=================
Aenea Grammars
=================

Grammars and vocabulary for use with Aenea (https://github.com/dictation-toolbox/aenea)

| Alex Roper
| alex@aroper.net
| http://github.com/calmofthestorm

Set up Aenea first.

These grammars all use Aenea's configuration system, which expects grammar configuration in PROJECT_ROOT/grammar_config/NAME.json and vocabulary configuration under PROJECT_ROOT/vocabulary_config/...

Most modules will let you change what you say to do something by editing the VALUE part of the commands mapping in their config files.

See Aenea's documentation for how to use vocabularies, but the best way is to look at the examples in this repository and adapt them to your needs.

Please feel free to post in the Dragonfly Google group https://groups.google.com/forum/#!forum/dragonflyspeech or to email me if you have questions about this system or issues getting it working. I don't use it as much as I used to, but I'm still happy to discuss getting it to work and improving it, particularly the setup instructions, and I've learned a great deal from other users already.

Multiedit
---------

Multiedit is a heavily modified version of the version from the dragonfly-modules repository, also by Christo Butcher (the author of Dragonfly). It supports chaining commands together (so you don't have to pause constantly while coding), repeats, and dynamic vocabulary via the vocabulary system.

VIM
-------------

A grammar inspired by multiedit that allows use of much of VIM's keyboard commands. VIM does not consist of commands and hotkeys; it is a language and must be treated as such. This vim grammar attempts to embrace this design rather than fighting it, by creating a grammar closely corresponding to VIM's. Like multiedit, you can chain commands together, and what you speak has a very simple mapping to VIM keystrokes. (del 5 down 5 up plop = d5j5kp). Also supports vocabulary, and integrates it seamlessly into VIM's mode system. This assumes that VIM is in normal mode when the command is executed, and will always restore normal mode when a command is executed. Unfortunately this grammar does not (yet) support rebinding verbal commands, nor rebinding VIM commands (if you use remap commands).

Awesome
-------

Lets you control the Awesome window manager. Supports rebinding.

Chromium
--------

Bindings for Chrome/Chromium. Should work via proxy or locally. Supports rebinding.
