# 3rd party
from flask import current_app, request
from flask_restx import Namespace, Resource, fields
from meshtastic import __main__ as meshtastic
import yaml


api = Namespace("Local Config", description="Config operations")

abstractConfig = api.model("AbstractConfig", {"*": fields.Wildcard(fields.String)})

configModel = api.model(
    "Config",
    {
        "owner": fields.String,
        "owner_short": fields.String,
        "ownerShort": fields.String(attribute="owner_short"),
        "channel_url": fields.String,
        "channelUrl": fields.String(attribute="channel_url"),
        "location": fields.Nested(
            api.model(
                "Location",
                {"alt": fields.Integer, "lat": fields.Float, "lon": fields.Float},
            )
        ),
        "config": fields.Nested(abstractConfig),
        "module_config": fields.Nested(abstractConfig),
    },
)


@api.route("")
class LocalConfig(Resource):
    @api.doc(description="Returns the configuration of the node connected via serial.")
    def get(self):
        config_text = meshtastic.export_config(current_app.interface)
        output = yaml.safe_load(config_text)
        return output

    @api.doc(
        description="Update the current configuration",
    )
    @api.expect(configModel)
    def post(self):
        configuration = request.json
        interface = current_app.interface
        node_id = interface.getMyUser()["id"]
        # following code reused from meshtastic.__main__
        # Line 399; if args.configure
        interface.getNode(node_id, False).beginSettingsTransaction()

        if "owner" in configuration:
            interface.getNode(node_id, False).setOwner(configuration["owner"])

        if "owner_short" in configuration:
            interface.getNode(node_id, False).setOwner(
                long_name=None, short_name=configuration["owner_short"]
            )

        if "channel_url" in configuration:
            interface.getNode(node_id).setURL(configuration["channel_url"])

        if "location" in configuration:
            alt = 0
            lat = 0.0
            lon = 0.0
            localConfig = interface.localNode.localConfig

            if "alt" in configuration["location"]:
                alt = int(configuration["location"]["alt"])
                localConfig.position.fixed_position = True
            if "lat" in configuration["location"]:
                lat = float(configuration["location"]["lat"])
                localConfig.position.fixed_position = True
            if "lon" in configuration["location"]:
                lon = float(configuration["location"]["lon"])
                localConfig.position.fixed_position = True
            interface.sendPosition(lat, lon, alt)
            interface.localNode.writeConfig("position")

        if "config" in configuration:
            localConfig = interface.getNode(node_id).localConfig
            for section in configuration["config"]:
                for pref in configuration["config"][section]:
                    meshtastic.setPref(
                        localConfig,
                        f"{section}.{pref}",
                        str(configuration["config"][section][pref]),
                    )
                interface.getNode(node_id).writeConfig(section)

        if "module_config" in configuration:
            moduleConfig = interface.getNode(node_id).moduleConfig
            for section in configuration["module_config"]:
                for pref in configuration["module_config"][section]:
                    meshtastic.setPref(
                        moduleConfig,
                        f"{section}.{pref}",
                        str(configuration["module_config"][section][pref]),
                    )
                interface.getNode(node_id).writeConfig(section)

        interface.getNode(node_id, False).commitSettingsTransaction()
        return "success"
