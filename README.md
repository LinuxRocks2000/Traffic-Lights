# Traffic Lights Server

This is a traffic lights programming system. It serves as an introduction to network programming and algorithms.

It manifests itself as a fairly minimal server written in Python which uses Tkinter for graphics. There will be several layers of API for increasingly advanced coders eventually, but for now it is just a very simple byte-based protocol. Send one byte (a letter), then data bytes if necessary. We don't support CSV yet, so for now you just send the character of it. In python, the syntax is `chr(number)`, and in C/C++ you just use an integer pointer (`&my_int`) passed into the `write` call. This is a fairly rough road, so I'll be adding a CSV version later (at the time of writing, it is late and I want to go to sleep).

Here's a quick table of commands:

| Command | Usage                                                        |
| ------- | ------------------------------------------------------------ |
| S       | Set a light. Next two bytes should be x and y of the intersection you're editing, and the next one after that should be a light position TOP/BOTTOM/LEFT/RIGHT (see macro table). The very last one should be a color RED/GREEN/YELLOW (macro table). |
| U       | Update the GUI. No arguments.                                |
| E       | Gracefully exit and allow another client to connect. You should close the socket at this point. |
| D       | Destroy the GUI. This is only for reference, it isn't implemented. |
| R       | Begin the GUI. This is only for reference, it isn't implemented. |

## Macros

In C, we have macros. In python, we can assign static variables to a class. These macros are true for all implementations:

| Macro name | Macro value |
| ---------- | ----------- |
| TOP        | 0           |
| BOTTOM     | 1           |
| LEFT       | 2           |
| RIGHT      | 3           |
| RED        | 1           |
| YELLOW     | 2           |
| GREEN      | 0           |

