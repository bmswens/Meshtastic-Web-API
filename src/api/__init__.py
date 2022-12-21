# 3rd party
from flask_restx import Api

# custom
from .nodes import api as nodes

api = Api(
    title="Meshtastic REST API",
    version="0.1",
    description="A RESTful interface for interacting with a Meshtastic node over serial connection.",
    contact="bmswens@gmail.com",
    license="GNU GENERAL PUBLIC LICENSE",

)

api.add_namespace(nodes, path="/nodes")