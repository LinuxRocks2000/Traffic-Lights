# Traffic Lights Server

It is nerd history that many great coders got their start in traffic engineering. Bill Gates had Traf-O-Data, and the less-known Phillip Ciccone re-did an entire city's traffic light systems (potentially apocryphalic?) in high school.

This doesn't really sound like a big list, but the impact this has on communities is incredible. Any young coder today wishes to prove their worth through something important, and that's one of them!

## Poor prose aside

To cut to the chase, this is a traffic lights programming system. It serves as an introduction to network programming and algorithms.

It manifests itself as a fairly minimal server written in Python which uses Tkinter for graphics. There will be several layers of API for increasingly advanced coders eventually, but for now it is just a very simple byte-based protocol. Send one byte (a letter), then data bytes if necessary. We don't support CSV yet, so for now you just send the character of it. In python, the syntax is `chr(number)`, and in C/C++ you just use an integer pointer (`&my_int`) passed into the `write` call. This is a fairly rough road, so I'll be adding a CSV version later (at the time of writing, it is late and I want to go to sleep).

Here's a quick table of commands:

| Command | Usage                                                        |
| ------- | ------------------------------------------------------------ |
| S       | Set a traffic. [gonna finish this later, just read my Python if you really want to use this, otherwise wait for me to finish it] |
|         |                                                              |
|         |                                                              |