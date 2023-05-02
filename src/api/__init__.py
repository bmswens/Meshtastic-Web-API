# 3rd party
from flask_restx import Api

# custom
from .nodeInfo import api as nodeInfo
from .localConfig import api as localConfig
from .serialPort import api as serialPort
from .messages import api as messages
from .cannedMessageModule import api as cannedMessage
from .positions import api as positions
from .mattermost import api as mattermost

api = Api(
    title="Meshtastic Web API",
    version="0.1",
    description="A web interface for interacting with a Meshtastic node over serial connection.",
    contact="bmswens@gmail.com",
    license="GNU GENERAL PUBLIC LICENSE",
    license_url="https://github.com/bmswens/Meshtastic-REST-API/blob/main/LICENSE",
)

api.add_namespace(nodeInfo, path="/node-info")
api.add_namespace(localConfig, path="/local-config")
api.add_namespace(serialPort, path="/serial-port")
api.add_namespace(messages, path="/messages")
api.add_namespace(cannedMessage, path="/canned-message-module-config")
api.add_namespace(positions, path="/positions")
api.add_namespace(mattermost, path="/mattermost")
