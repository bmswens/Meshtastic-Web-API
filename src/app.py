# built in
import argparse
import json
import os

# 3rd party
from flask import Flask
import meshtastic.serial_interface

# custom
from api import api
import db


def create_app(connect=True):
    # flask init
    app = Flask(__name__)
    # meshtastic interface that all sub modules will use
    interface = None
    if connect:
        interface = meshtastic.serial_interface.SerialInterface()
    db_path = db.start()
    app.interface = interface
    app.db = db.Database(db_path)
    api.init_app(app)
    return app, api


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(
        description="Start the server or export the swagger.json"
    )
    parser.add_argument("--export", nargs="?", dest="export", default=False, const=True)
    args = parser.parse_args()
    if args.export:
        app, api = create_app(False)
        app.config["SERVER_NAME"] = "bmswens.github.io/Meshtastic-Web-API/"
        with app.app_context():
            with open("swagger.json", "w") as output:
                output.write(json.dumps(api.__schema__, indent=2))
    else:
        app, api = create_app()
        app.run(host="0.0.0.0")
