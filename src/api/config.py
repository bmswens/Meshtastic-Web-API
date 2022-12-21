# 3rd party
from flask import current_app, request
from flask_restx import Namespace, Resource
from meshtastic import __main__ as meshtastic
import yaml

# custom
from .utils import clean_position

api = Namespace("config", description="Config operations")

@api.route("")
@api.doc(
    description="Returns the configuration of the node connected via serial."
)
class GetConfig(Resource):
    def get(self):
        config_text = meshtastic.export_config(current_app.interface)
        output = yaml.safe_load(config_text)
        print(config_text)
        return output