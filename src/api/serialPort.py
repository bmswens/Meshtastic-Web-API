# 3rd party
from flask import current_app
from flask_restx import Namespace, Resource, fields

api = Namespace("Serial Port", description="Information about the serial connection")

portModel = api.model(
    "Port", {"port": fields.String(example="COM4, /dev/ttyUSB0, etc.")}
)


@api.route("")
class Port(Resource):
    @api.doc(
        description="Returns JSON containing the port the device is connected on.",
    )
    @api.response(200, "Success", portModel)
    def get(self):
        return {"port": current_app.interface.devPath}
