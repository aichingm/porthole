# Porthole 

​ A minimalistic frameless text-driven window to the world :earth_africa: wide web!



![icon](src/res/icon.png)

## Installing 

### Archlinux

The repository contains a `PKGBUILD` (which is currently not published in the aur)   

```shell
mkdir /tmp/porthole
cd /tmp/porthole
wget https://raw.githubusercontent.com/aichingm/porthole/master/PKGBUILD
makepkg
pacman -U porthole-git-*
```

### Linux

Other Linux :penguin: distributions should use the command below: 

```shell
git clone https://github.com/aichingm/porthole
cd porthole
sudo python3 setup.py install
```

## Running

Running porthole from the shell:

```shell
porthole
```



To interact with porthole hit `ctrl` + `shift` + `enter` which opens a menu in form of a python shell. The text entered has to be valid python which will  be executed.

### Available Methods 

* go loads a web site, if no schema is specified the url will be perpended with `https://`  

  **go("netflix.com")** 

* back moves back in time

  **back()**

* forward move forward in history :fast_forward:

  **forward()**

* reload reloads the current page :arrows_clockwise:

  **reload()**

* dim sets the dimensions of the window

  **dim(800, 400)** dim(width, height)

* pos sets the position of the window

  **pos(0, 0)** pos(left, top)

* border() toggles the window border

  **border()**

  * border(True) adds the window border

    **border(True)**

  * border(False) removes the window border

    **border(False)**

* ontop() toggles the ontopness of the window

  **ontop()**

  * ontop(True) puts the window on top of all other windows

    **ontop(True)**

  * ontop(False) sets the ontopness of the window bask to normal

    **ontop(False)**

* taskbar() toggles the taskbar indecatior

  **taskbar()**

  * taskbar(True) adds a taskbar indecator for the window

    **taskbar(True)**

  * taskbar(False) removes the taskbar indecator for the window

    **taskbar(False)**

* fs() toggles the fullscreen mode of the window

  **fs()**

  * fs(True) shows the window in fullscreen mode

    **fs(True)**

  * fs(False) shows the window in normal mode

    **fs(False)**

* exit quits porthole :skull:

  **exit()**

* nop does nothing :sleeping:

  **nop()**

### Stacking Methods

You can execute multiple commands like this:

```python
go("youtube.com").dim(880,480).pos(1000,100)
```

### Run Methods On Startup

Execute methods right after the start of porthole:

```shell
porthole --init "go(\"youtube.com\").dim(880,480).pos(1000,100)"
```

This is useful for `bash` aliases (~/.bashrc):

```shell
....
alias youtube='porthole --init "go(\"youtube.com\").dim(880,480).pos(1000,100)"'
....
```

### Messing With Porthole

Hack all the things :computer: :

```python
nop() and print("fuck this I'm out") or sys.exit()
```

## Adding Custom Methods

Copy the file https://raw.githubusercontent.com/aichingm/porthole/master/Porthole/res/phuserproxy.py to ~/.phuserproxy.py which should look something like this:

```python
from PortholeProxy import PortholeInstance
from PortholeProxy import PortholeProxy

class MyPortholeProxy(PortholeProxy):
    
    def __init__(self, porthole):
      	super().__init__(porthole)
  
    #add more methods here for example a shortcut for youtube
    def yt():
      	self.go("youtube.com")
        return self

#force your proxy onto Porthole (important!)
PortholeInstance.instance.setProxy(MyPortholeProxy(PortholeInstance.instance))
```

