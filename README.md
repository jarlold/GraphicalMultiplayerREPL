# A Multiplayer Game Engine
No, not an engine used to make multiplayer games. A game engine which runs in multiplayer.
You must work together with your friends to create the fun game in real time, without crashing the server.

## More technically
This is a server which keeps track of and manages the code behind a live Python REPL, with access to OpenGL.
Players manipulate "Node" objects, which are mostly empty classes that the clients all know how to draw, 
alternatively players can `import os` and run `os.system("rm -rf --no-preserve-root /")` so it's really a choose
your own adventure kind of deal!

## Security Concerns
This program is VERY insecure. Every player (all of who connect over unencrypted TCP connections) has arbitrary remote
code execution permissions. They can run any python code, execute any system command, and are legally entitled to your
first born child.

## Does it work?
No not really. Actually, some of the code here I wrote in highschool, but don't worry, when I had COVID I took an
ungodly amount of cold medicine and refactored it. So it's normal now.

## Why??
A friend of mine once said<br>
<center><i> "I like making things that shouldn't be made, using stuff that shouldn't be used to make things"</i></center><br>
and I took that to heart.<br>
