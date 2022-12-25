# 3rd party
from flask import current_app, request
from flask_restx import Namespace, Resource, fields, marshal

api = Namespace("Messages", description="Sending and recieving text messages")

messageModel = api.model(
    "Sent Message",
    {
        "text": fields.String(
            required=True, example="Hello world!", description="The text to send"
        ),
        "destinationId": fields.String(
            default="^all", description="Where to send this message"
        ),
        "wantAck": fields.Boolean(
            default=True,
            description="If you want the message sent in a reliable manner (with retries and ack/nak provided for delivery)",
        ),
        "wantResponse": fields.Boolean(
            default=False,
            description="If you want the service on the other side to send an application layer response",
        ),
        "channelIndex": fields.Integer(
            default=0, description="The channel to send the message on"
        ),
    },
)

recMessageModel = api.model(
    "Recieved Message",
    {
        "uuid": fields.Integer(description="Interal database UUID"),
        "sender": fields.String(
            description="The ID of the sender", example="!9388f81c"
        ),
        "target": fields.String(
            description="Intended target of the message", example="^all"
        ),
        "text": fields.String(
            description="The content of the message", example="Hello world!"
        ),
        "channel": fields.Integer(description="The channel index", example="0"),
        "timestamp": fields.DateTime(
            description="ISO8601 formatted datetime",
            example="2022-12-23T14:51:15.784133",
        ),
    },
)


@api.route("")
class TextMessage(Resource):
    @api.doc(description="Send a message on a channel, defaults to primary channel")
    @api.expect(messageModel)
    def post(self):
        interface = current_app.interface
        localNode = interface.localNode
        message = marshal(request.json, messageModel)
        channelIndex = message["channelIndex"]
        if not message["text"]:
            return {"message": "'text' must be in body"}, 400
        elif channelIndex < 0 or channelIndex > len(localNode.channels) - 1:
            return {"message": f"channelIndex {channelIndex} out of range"}, 400
        # channelSettings objects are empty when converted to strings if unconfigured
        elif not str(localNode.channels[channelIndex].settings):
            return {"message": f"Channel {channelIndex} not configured"}, 404
        interface.sendText(**message)
        return {"message": "success"}, 200

    @api.doc(description="Get messages stored in the database")
    @api.marshal_with(recMessageModel)
    @api.param("dm", description="Shows only direct messages")
    @api.param("limit", description="Limit how many messages to output")
    def get(self):
        interface = current_app.interface
        params = request.args.to_dict()
        dm = None
        if "dm" in params:
            user = interface.getMyUser()
            dm = user["id"]
        limit = params.get("limit")
        with current_app.db as db:
            messages = db.get_messages(limit, dm)
        return messages
