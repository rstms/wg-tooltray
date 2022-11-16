from pystray import Icon, Menu, MenuItem
import signal
from pathlib import Path

from PIL import Image, ImageDraw


class Network():
    def __init__(self, name, commands):
        self.name = name
        self.start_cmd = commands['start']
        self.stop_cmd = commands['stop']

    def menu(self):
        return MenuItem(self.name, self.on_click, self.is_checked)

    def start(self):
        run(self.start_cmd, shell=True)
        return self.is_checked()

    def stop(self):
        run(self.stop_cmd, shell=True)
        return self.is_checked()

    def is_checked(self, item):
        proc = run(['ip', 'link', 'show', self.name], text=True, check=True, capture_output=True)
        pre, _, mid = proc.stdout.partition('<')
        status, _, _ = mid.partition('>')
        return 'UP' in status.split(',')
        print(f'is_checked {item} -> {ret}')

    def on_click(self, icon, item):
        if self.is_checked():
            return self.stop()
        else:
            return self.start()


class TrayIcon():
    def __init__(self, name='Wireguard VPN', networks={}, callback=None):

        image_file = Path(__file__).parent / 'icon.png'
        self.name = name
        self.networks = networks
        self.callback = callback
        self.state = False
        self.icon = Icon(
            self.name,
            icon=Image.open(str(image_file)),
            menu = self.get_menu()
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

    def get_menu(self):
        _menu = [MenuItem(self.name,self.on_clicked), Menu.SEPARATOR]
        _menu.extend([Network(if_name, commands).menu() for if_name, commands in self.networks.items()])
        _menu.extend([Menu.SEPARATOR, MenuItem("Exit", self.on_clicked)])
        return _menu

    def on_clicked(self, icon, item):
        if item.text == 'Exit':
            self.stop()
            signal.raise_signal(signal.SIGINT)
        else:
            self.update_menu()

    def run(self):
        self.icon.run()
