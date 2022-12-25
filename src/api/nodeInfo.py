# 3rd party
from flask import current_app, request
from flask_restx import Namespace, Resource, fields

api = Namespace("Node Info", description="Information about the node(s)")

# Node Info Models

PositionModel = api.model(
    "Position",
    {
        "altitude": fields.Integer,
        "latitude": fields.Float,
        "longitude": fields.Float,
        "time": fields.Integer,
    },
)

UserModel = api.model(
    "User",
    {
        "id": fields.String(
            example="!55c77c48", description="Predefined ID for the device."
        ),
        "longName": fields.String(
            example="Meshtastic Device 1",
            description="User defined long name of the device.",
        ),
        "shortName": fields.String(
            example="MD1", description="User defined short name of the device."
        ),
        "macaddr": fields.String(
            example="lLVVx3xI", description="Predfined mac address for th device."
        ),
        "hwModel": fields.String(
            example="TBEAM", description="predefined hardware model of th device."
        ),
    },
)

DeviceMetricsModel = api.model(
    "Device Metrics",
    {
        "batteryLevel": fields.Integer(
            example=77, description="The battery level of the device."
        ),
        "voltage": fields.Float(
            example=4.159, description="The current voltage of the device."
        ),
        "channelUtilization": fields.Float(
            example=5.4733334, description="Current channel utilization."
        ),
        "airUtilTx": fields.Float(example=3.154972, description="I'm not quite sure."),
    },
)

NodeInfoModel = api.model(
    "Node Info",
    {
        "num": fields.Integer(
            example=1439136840, description="Serial number of the device."
        ),
        "user": fields.Nested(UserModel),
        "position": fields.Nested(PositionModel),
        "lastHeard": fields.Integer(
            example=1671952630,
            description="Time the node was last heard, as seconds since epoch.",
        ),
        "deviceMetrics": fields.Nested(DeviceMetricsModel),
    },
)


@api.route("")
class NodeInfo(Resource):
    @api.doc(description="Returns all the known nodes as list.")
    @api.marshal_with(NodeInfoModel)
    def get(self):
        nodes = current_app.interface.nodes
        return [nodes[node] for node in nodes]


@api.route("/<node>")
class SingleNodeInfo(Resource):
    @api.doc(
        description="Returns info of a node in JSON format.",
        params={"node": "The Node ID, Long Name, Short Name, or MAC Address."},
        responses={200: "OK", 404: "Node not found"},
    )
    @api.marshal_with(NodeInfoModel)
    def get(self, node):
        nodes = current_app.interface.nodes
        for nodeNum in nodes:
            nodeInfo = nodes[nodeNum]
            accepted_names = [
                nodeNum,
                nodeInfo["user"].get("longName"),
                nodeInfo["user"].get("shortName"),
                nodeInfo["user"].get("macaddr"),
            ]
            if node in accepted_names:
                return nodeInfo, 200
        return {"message": "Node not found"}, 404
