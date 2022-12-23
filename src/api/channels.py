# 3rd party
from flask import current_app, request
from flask_restx import Namespace, Resource, fields, marshal

api = Namespace("channel", description="Channel-centric operations, includes messaging and configuration.")

messageModel = api.model("Message", {
    "text": fields.String(
        required=True,
        example="Hello world!",
        description="The text to send"
    ),
    "destinationId": fields.String(
        default="^all",
        description="Where to send this message"
    ),
    "wantAck": fields.Boolean(
        default=True,
        description="If you want the message sent in a reliable manner (with retries and ack/nak provided for delivery)"
    ),
    "wantResponse": fields.Boolean(
        default=False,
        description="If you want the service on the other side to send an application layer response"
    ),
    "channelIndex": fields.Integer(
        default=0,
        description="The channel to send the message on"
    )
})

@api.route("/messages")
class TextMessage(Resource):
    @api.doc(
        description="Send a message on a channel, defaults to primary channel"
    )
    @api.expect(messageModel)
    def post(self):
        interface = current_app.interface
        localNode = interface.localNode
        message = marshal(request.json, messageModel)
        channelIndex = message["channelIndex"]
        if not message["text"]:
            return {"message": "'text' must be in body"}, 400
        elif channelIndex < 0 or channelIndex > len(localNode.channels) - 1:
            return {"message": f'channelIndex {channelIndex} out of range'}, 400
        # channelSettings objects are empty when converted to strings if unconfigured
        elif not str(localNode.channels[channelIndex].settings):
            return {"message": f'Channel {channelIndex} not configured'}, 404
        interface.sendText(**message)
        return { "message": "success" }, 200
        