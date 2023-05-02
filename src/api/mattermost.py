# built in
import os

# 3rd party
from flask import current_app, request
from flask_restx import Namespace, Resource, fields, marshal
import requests

api = Namespace("Mattermost", description="Extend Mattermost messages to Meshtastic.")

mattermostModel = api.model(
    "From Mattermost",
    {
        "channel_id": fields.String(
            required=False,
            example="hawos4dqtby53pd64o4a4cmeoo",
            description="Mattermost Channel ID"
        ),
        "channel_name": fields.String(
            required=False,
            example="town-square",
            description="Mattermost Channel Name"
        ),
        "team_domain": fields.String(
            required=False,
            example="someteam",
            description="Mattermost Team Name"
        ),
        "team_id": fields.String(
            required=False,
            example="kwoknj9nwpypzgzy78wkw516qe",
            description="Mattermost Team ID"
        ),
        "post_id": fields.String(
            required=False,
            example="axdygg1957njfe5pu38saikdho",
            description="Mattermost Post ID"
        ),
        "text": fields.String(
            required=True,
            example="some+text+here",
            description="Text to send to Meshtastic"
        ),
        "timestamp": fields.Integer(
            required=False,
            example=1445532266,
            description="Mattermost timestamp for message"
        ),
        "token": fields.String(
            required=True,
            example="zmigewsanbbsdf59xnmduzypjc",
            description="Mattermost token, changes per deployment"
        ),
        "trigger_word": fields.String(
            required=False,
            example="some",
            description="Trigger word that activated the webhook"
        ),
        "user_id": fields.String(
            required=False,
            example="rnina9994bde8mua79zqcg5hmo",
            description="Mattermost User ID"
        ),
        "user_name": fields.String(
            required=True,
            example="somename",
            description="Mattermost Usernam"
        )
    }
)

@api.route("")
class MattermostMessage(Resource):
    @api.doc(description="Send a message from Mattermost to Meshtastic")
    @api.expect(mattermostModel)
    def post(self):
        interface = current_app.interface
        from_mattermost = marshal(request.json, mattermostModel)
        if not from_mattermost["text"]:
            return {"message": "'text' must be in body"}, 400
        if os.getenv("MATTERMOST_TOKEN") != from_mattermost["token"]:
            return {"message": "token does not match"}, 403
        text = f'FROM: {from_mattermost["user_name"]}\n{from_mattermost["text"]}'
        interface.sendText(text=text, wantAck=True)
        return {"message": "success"}, 200


def onMessage(packet, interface):
    sender = packet["fromId"]
    text = packet["decoded"]["payload"].decode()
    senderName = sender
    nodes = interface.nodes
    # try and get a long name for the sender
    for nodeNum in nodes:
        nodeInfo = nodes[nodeNum]
        if nodeNum == sender:
            senderName = nodeInfo["user"].get("longName")
    # post that data
    body = {
        "text": text,
        "username": senderName 
    }
    url = os.getenv("MATTERMOST_WEBHOOK")
    requests.post(url, json=body)