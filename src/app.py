# 3rd party
from flask import Flask
import meshtastic.serial_interface

# custom
from api import api


def create_app():
    # flask init
    app = Flask(__name__)
    # meshtastic interface that all sub modules will use
    interface = meshtastic.serial_interface.SerialInterface()
    app.interface = interface
    api.init_app(app)
    return app

if __name__ == "__main__": # pragma: no cover
    app = create_app()
    app.run()