# 3rd party
from flask import current_app, request
from flask_restx import Namespace, Resource, fields, marshal

api = Namespace(
    "Canned Message Module Config", description="Canned message module configuration."
)

canned_message_model = api.model(
    "Canned Message Config",
    {
        "messages": fields.String(
            description="Predefined messages for canned message module separated by '|' characters.",
            required=True,
            example="My new message",
        )
    },
)


@api.route("")
class CannedMessage(Resource):
    @api.doc(description="Get the current canned message")
    @api.marshal_with(canned_message_model)
    def get(self):
        message = current_app.interface.localNode.get_canned_message()
        message = message[message.find("'") + 1 : message.rfind("'")]
        return {"messages": message}

    @api.doc(description="Update the current canned message")
    @api.expect(canned_message_model)
    def post(self):
        body = request.json
        if "messages" not in body:
            return {"message": "Missing 'messages' in body"}, 400
        localNode = current_app.interface.localNode
        localNode.set_canned_message(body["messages"])
        return {"messages": body["messages"]}
