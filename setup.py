from setuptools import setup

APP = ['daisy Sms fix.py']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',  # опціонально
    'packages': [],           # додаткові пакети, якщо треба
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
