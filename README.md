# Flint - A Super Paper Mario Text Editor
## About this editor
Heya guys this is the first release an SPM tool to come out of my **CragonSuit** named **Flint** (after Flint Cragely of course).\
This tool allows you to edit all of the text found in Super Paper Mario and preview how it will look in game before you load your 
Riivolution Patches.\
<img width="720" height="480" alt="Overview.png" src="https://github.com/user-attachments/assets/adcd6532-f575-4ee2-bbeb-240484fe1a51" />


I added some nice features that hopefully allow script writers to enjoy and relax while writing dialogs for their custom games.\
Such features include:
- Playing BGM's in the editor (loop and loop all supported)
- Sound Effects for the menus to mimmick the game
- Dark Mode
- Custom theme creation (for those who's eyes have specific taste)
- Importing/Exporting themes to share
- Editor Language (currently only supports English this feature will be implemented at a later date!)
<img width="432" height="410" alt="Settings.png" src="https://github.com/user-attachments/assets/cc387ecd-9673-46f8-8a76-fbff40d87d3f" />


## Currently supported Operating Systems
**Windows**:
- Windows 10 and Window 11 have been tested and are working with icon support

**Linux**:
- Ubuntu, Fedora and Arch Linux have been tested and are working with icon support

**Mac OS**:
- Mac OS 10.X.X has been tested and is working with icon support (I need more people to test other versions of Mac OS)

## Build Intructions
First things first make sure you have python3! I know it may seem obvious but people forget this sometimes so here's a link:\
https://www.python.org/downloads/

Also be sure to pip install the necessary packages for building and or running:
```bash
pip install pyqt5
pip install pyinstaller
pip list
```

If you want to build it yourself you can use pyinstaller and use the following based on your Operating System:

**Windows**:
```powershell
pyinstaller --onefile --noconsole --icon=Packaged_Resources/Images/Editor/Icon.ico --add-data "Packaged_Resources:Packaged_Resources" src/Flint.py
```
**Linux**:
```bash
pyinstaller --onefile --noconsole --add-data "Packaged_Resources:Packaged_Resources" src/Flint.py
```
**Mac OS**:
```bash
pyinstaller --onefile --noconsole --icon=Packaged_Resources/Images/Editor/Icon.icns --add-data "Packaged_Resources:Packaged_Resources" src/Flint.py
```
Building from a spec file (one created by the builder or the one provided from the github):
```powershell
pyinstaller --clean Flint.spec
```

When built the programs structure should look like this:

```
Flint V1.3
├── Audio
│   ├── BGM
│   │   ├── BGM1.mp3
│   │   └── ...
│   ├── Effects
│   │   ├── Sound1.mp3
│   │   └── ...
├── Themes
│   ├── Theme1.json
│   └── ...
├── Flint.exe
└── Settings.ini
```


## Debugger for contributors
When you remove `--noconsole` from the build commands you can get access to the debugger. It can be used to print to the 
console what the program is doing so any issues or odities can be solved quickly. It's very easy to read and implement 
here are the types you'll encounter:
- **debug**: standard debug messages printed in blue
- **info**: descriptive debug messages printed in green
- **warning**: non critical issue debug message leading to odd behaviour but not broken states (i.e a sound file can't be read) printed in yellow
- **error**: issue debug message which causes problems that effect usability printed in red

## Console Attachment
You can attach pretty much any console of choice for the debugger in case you have a prefered one! Below I'll 
list the supported consoles and how they can be used to launch and debug the program\
*Note if running from the Flint.py file the debugger is always active unlike build versions which will only work if built without --noconsole*

### Powershell and CMD
Install on Windows python3:
```powershell
winget install --id Python.Python.3.13 # or use the installer: https://www.python.org/downloads/windows/
python --version
pip --version
```
Running from the python interpreter in Powershell/CMD:
```powershell
# Install necessary dependancies
pip install pyqt5

# Run the program
python Flint.py
```
Running the build version in Powershell/CMD:
```powershell
.\Flint.exe
```
*Note if built without the `--noconsole` it will show debug messages when launched in Powershell/CMD or if it's just double clicked!* 

### Linux Bash
Install python3 on linux:

Debian
```bash
sudo apt update
sudo apt install python3 python3-pip -y
python3 --version
```
Fedora:
```bash
sudo dnf install python3 python3-pip -y
python3 --version
```
Arch:
```bash
sudo pacman -Syu python python-pip
python --version
```

Running from the python interpreter in the Linux Bash:
```bash
# Create a venv and install the dependancies
python -m venv flintvenv
source flintvenv/bin/activate
pip install pyqt5

# Run the program
python3 Flint.py
```
Running the build version in the Linux Bash:
```bash
./Flint
```
*Note if built without the `--noconsole` it will show debug messages when launched in Powershell/CMD or if it's just double clicked!* 

### WSL2 instructions
*WSL2 should have WSLg enabled by default if not enable it in your WSL settings*

Link to Debian MS Store:
```html
https://apps.microsoft.com/detail/9msvkqc78pk6?hl=en-US&gl=US
```

Open Powershell in admin mode and use the following commands:
```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```
Reboot your PC once these are done (**make sure in your bios hardware based virtualization is turned on!**)

Once rebooted use this command in the admin Powershell
```powershell
wsl --set-default-version 2
```

If you recieve this error: 
```powershell
Installing, this may take a few minutes...
WslRegisterDistribution failed with error: 0x800701bc
Error: 0x800701bc WSL 2 requires an update to its kernel component.
For information please visit https://aka.ms/wsl2kernel
```
You'll need to install the Linux kernel update package:
```
https://learn.microsoft.com/en-us/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package
```
\
**Offical MS Reference for WSL if the above doesn't resolve issues:**
```
https://learn.microsoft.com/en-us/windows/wsl/install-manual
```
\
Following a sucessful WSL installation on your system install the following packages:
```bash
# python and pyqt5
sudo apt install python3-pyqt5
# gstreamer for linux audio handeling
sudo apt install gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly
```

Running from the python interpreter in WSL2:
```bash
python3 Flint.py
```

Running the build version in WSL2:
```bash
./Flint
```


### MSYS2 install instructions
Link to MSYS2's website:
```html
https://www.msys2.org/
```

Running from the python interpreter in MSYS2 MINGW64:
```bash
# Install the necessary depndancies
pacman -Syu
pacman -S mingw-w64-x86_64-python
pacman -S mingw-w64-x86_64-python-pyqt5
pacman -S mingw-w64-x86_64-qt5-multimedia

# Run the program
python3 Flint.py
```

Safety intall if dependencies are failing:
```bash
pacman -S mingw-w64-x86_64-qt5-base mingw-w64-x86_64-qt5-tools mingw-w64-x86_64-qt5-multimedia
```

Running the build version in MSYS2 MINGW64:
```bash
./Flint.exe
```

### Cygwin install instructions
Link to Cygwin's website:
```html
https://www.cygwin.com/
```

When installing Cygwin install the following packages:
```bash
...(I'll write this I swear)
```

Running from the python interpreter in Cygwin:
```bash
/cygdrive/c/Users/you/AppData/Local/Programs/Python/Python313/python.exe C:\Users\you\...\Flint\Flint.py
```

Running the build version in Cygwin:
```bash
/cygdrive/c/Users/you/.../Flint\ V1.0/Flint.exe
```

## What the future holds...
So in the future of this project I hope to add the following:
- Live Animation player for bubbles instead of symbolic icons
- Even cleaner and more thematic documentation
- Music and Sound Effects using the in game formats across all platforms *this will tie into something later!*

Stay tuned for all this stuff. Hopefully the current build is still enjoyable experience to use! 

## Special Thanks
Thank you for checking out the first to hopefully many tools to come from me!\
If you'd like to support my work you can do so on Ko-Fi but feel no obligation to of course: https://ko-fi.com/luma48 \
For more from me you can visit my YT Channel and find more of my to be content: https://www.youtube.com/@luma4826 \
<img width="220" height="220" alt="Luma48.png" src="https://github.com/user-attachments/assets/a9873609-5807-4053-b7a4-bf093181abb5" />



\
I'd like the thank @SandalChannel from Minute Games for all the Luma artwork you see, go ahead and check him out on his socials:\
https://www.youtube.com/@SandalChannel \
<img width="220" height="220" alt="Sandal.png" src="https://github.com/user-attachments/assets/2145b191-6076-43e6-988b-b7050a2b1b0e" />


