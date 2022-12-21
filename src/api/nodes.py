# 3rd party
from flask import current_app
from flask_restx import Namespace, Resource

# custom
from .utils import clean_position

api = Namespace("nodes", description="Node-centric operations")

@api.route("/all")
@api.doc(
    description="Returns the IDs of all known node as a list."
)
class AllNodes(Resource):
    def get(self):
        return [nodeID for nodeID in current_app.interface.nodes]


@api.route("/info/<node>")
@api.doc(
    description="Returns info of a node in JSON format.",
    params={"node": "The Node ID, Long Name, Short Name, or MAC Address."},
    responses={200: "OK", 404: "Node not found"}
)
class Info(Resource):
    def get(self, node):
        nodes = current_app.interface.nodes
        for nodeNum in nodes:
            nodeInfo = nodes[nodeNum]
            accepted_names = [
                nodeNum,
                nodeInfo['user'].get('longName'),
                nodeInfo['user'].get('shortName'),
                nodeInfo['user'].get('macaddr')
            ]
            if node in accepted_names:
                info = dict(**nodeInfo)
                info['position'] = clean_position(info['position'])
                return info, 200
        return {"message": "Node not found"}, 404
