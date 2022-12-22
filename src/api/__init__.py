# 3rd party
from flask_restx import Api

# custom
from .nodes import api as nodes
from .config import api as config
from .serial import api as serial
from .channels import api as channels

api = Api(
    title="Meshtastic Web API",
    version="0.1",
    description="A web interface for interacting with a Meshtastic node over serial connection.",
    contact="bmswens@gmail.com",
    license="GNU GENERAL PUBLIC LICENSE",
    license_url="https://github.com/bmswens/Meshtastic-REST-API/blob/main/LICENSE"
)

api.add_namespace(nodes, path="/nodes")
api.add_namespace(config, path="/config")
api.add_namespace(serial, path="/serial")
api.add_namespace(channels, path="/channel")