# 3rd party
from flask_restx import Api

# custom
from .nodeInfo import api as nodeInfo
from .localConfig import api as localConfig
from .serialPort import api as serialPort
from .text import api as text

api = Api(
    title="Meshtastic Web API",
    version="0.1",
    description="A web interface for interacting with a Meshtastic node over serial connection.",
    contact="bmswens@gmail.com",
    license="GNU GENERAL PUBLIC LICENSE",
    license_url="https://github.com/bmswens/Meshtastic-REST-API/blob/main/LICENSE"
)

api.add_namespace(nodeInfo, path="/nodeInfo")
api.add_namespace(localConfig, path="/localConfig")
api.add_namespace(serialPort, path="/serialPort")
api.add_namespace(text, path="/text")
