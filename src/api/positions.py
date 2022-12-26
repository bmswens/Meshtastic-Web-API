# 3rd party
from flask import current_app, request
from flask_restx import Namespace, Resource, fields, marshal

api = Namespace(
    "Positions", description="Get information about the positions of nodes."
)

# models
PositionModel = api.model(
    "Position",
    {
        "uuid": fields.Integer(
            description="Interal UUID of the record.", example=111234
        ),
        "sender": fields.String(
            description="Node that the position is for.", example="!55c77c48"
        ),
        "target": fields.String(
            description="Who the position update was intended for, often '^all'.",
            example="^all",
        ),
        "altitude": fields.Integer(description="Altitude of the node.", example=327),
        "latitude": fields.Float(
            description="Latitude of the node, in decimal degrees.", example=33.5415
        ),
        "longitude": fields.Float(
            description="Longitude of the node, in decimal degrees.", example=112.3755
        ),
        "timestamp": fields.DateTime(
            description="ISO8601 formatted datetime",
            example="2022-12-23T14:51:15.784133",
        ),
    },
)


@api.route("")
class Positions(Resource):
    @api.doc(description="Get position entries from the database, most recent first.")
    @api.marshal_with(PositionModel)
    def get(self):
        with current_app.db as db:
            return db.get_positions()

@api.route("/<node>")
class NodePosition(Resource):
    @api.doc(description="Get the positions of a single node, by name, ID, etc.")
    @api.marshal_with(PositionModel)
    def get(self, node):
        interface = current_app.interface
        if node not in interface.nodes:
            found = False
            for nodeId in interface.nodes:
                nodeInfo = interface.nodes[nodeId]
                names = [
                    nodeInfo['user']["longName"],
                    nodeInfo['user']['shortName'],
                    nodeInfo['user']['macaddr']
                ]
                if node in names:
                    found = True
                    node = nodeId
                    break
            if not found:
                return {}, 404
        with current_app.db as db:
            return db.get_positions(node=node)
