python -m nuitka 'main.py' --follow-imports --include-data-dir='C:\Users\juozas\Code\arp-souls\assets'='.\assets' --include-package=arcade.gl.backends.opengl --include-package=mido.backends.rtmidi --standalone

# onefile
python -m nuitka 'main.py' --follow-imports --include-data-dir='C:\Users\juozas\Code\arp-souls\assets'='.\assets' --include-package=arcade.gl.backends.opengl --include-package=mido.backends.rtmidi  --onefile-windows-splash-screen-image='assets/loading-screen.png' --windows-icon-from-ico='assets/icon.png' --onefile

# attach console
python -m nuitka 'main.py' --follow-imports --include-data-dir='C:\Users\juozas\Code\arp-souls\assets'='.\assets' --include-package=arcade.gl.backends.opengl --include-package=mido.backends.rtmidi --windows-console-mode=attach --onefile-windows-splash-screen-image='assets/loading-screen.png' --windows-icon-from-ico='assets/icon.png' --onefile

# logs
# python -m nuitka 'main.py' --follow-imports --include-data-dir='C:\Users\juozas\Code\arp-souls\assets'='.\assets' --include-package=arcade.gl.backends.opengl --include-package=mido.backends.rtmidi --windows-force-stderr-spec='{PROGRAM}/logs.txt' --windows-force-stdout-spec='{PROGRAM}/output.txt' --onefile-windows-splash-screen-image='assets/loading-screen.png' --windows-icon-from-ico='assets/icon.png' --onefile