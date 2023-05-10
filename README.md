# filemanager
ONLY RUNS ON LINUX.

We've done nothing too complicated. We generate a simple internal filesystem representation of an existing (os based) filesystem using BFS, and then we make virtual updates to items there, and reflect those changes in the actual os provided filesystem.

The program features a simple gui made using tkinter and a base cli application as well. 

This, however, only runs on linux due to Windows' in built security features, understandably. It is a security risk to let some python application scan your filesystem. It's currently tested on arch linux, and we've verified that it DOES NOT work on windows. 

#Usage and installation
1. Install arch linux (if you do not want to go through this, we're sure that it could work on Ubuntu as well) via a virtual machine or sshing into an online linux shell. Perhaps wine would work as an appropriate emulator, though that also gets in the way with permissions.
2. Make sure tkinter is installed, along with shutils
3. Run application.py using python3.10
4. You will be prompted with a cli/gui statement
5. Typing cli will give you a cli, and gui will give you a gui
6. Information for using the cli is available by typing h and then enter
7. The gui is used by entering an object name, and (if needed) a user-provided tag
