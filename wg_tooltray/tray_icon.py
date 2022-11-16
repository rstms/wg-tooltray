from pystray import Icon, Menu, MenuItem
import signal
from pathlib import Path

from PIL import Image, ImageDraw


class TrayIcon():
    def __init__(self, name='Wireguard VPN', networks=[], callback=None):

        self.networks = {network:False for network in networks} 
        image_file = Path(__file__).parent / 'icon.png'
        self.callback = callback
        self.state = False
        self.icon = Icon(
            name,
            icon=Image.open(str(image_file)),
            menu = Menu(
                MenuItem(name,self.on_clicked),
                Menu.SEPARATOR,
                MenuItem("Exit", self.on_clicked, checked = lambda item: self.state)
            ) 
        )

    def __enter__(self):
        self.icon.run_detached()
        return self

    def __exit__(self, *args, **kwargs):
        if self.icon:
            self.icon.stop()
    
    def stop(self):
        self.icon.stop()
        self.icon = None

    def on_clicked(self, icon, item):
        if item.text in self.networks.keys():
            print(f"clicked: {item.text}")
        elif item.text == 'Exit':
            self.stop()
            signal.raise_signal(signal.SIGINT)

    def run(self):
        self.icon.run()
