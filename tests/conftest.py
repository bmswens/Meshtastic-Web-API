# built in
import os
from unittest.mock import MagicMock
import datetime

# 3rd party
from meshtastic.serial_interface import SerialInterface
from meshtastic.mesh_interface import MeshInterface
from meshtastic.node import Node
from meshtastic.channel_pb2 import Channel
import pytest

# custom
# add to os.sys.path so that we don't have to make a package
this_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(this_dir), "src")
os.sys.path.append(src_dir)
from app import create_app
import db


@pytest.fixture()
def app():
    # mock SerialInterface to always return a MeshInterface whithout
    # trying to connect over serial
    SerialInterface.__init__ = lambda x: None

    app, api = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # mock out the meshtastic interface
    # code yoinked from meshtastic tests
    iface = MagicMock(autospec=MeshInterface)
    anode = Node("foo", "bar")

    nodes = {
        "!9388f81c": {
            "num": 2475227164,
            "user": {
                "id": "!9388f81c",
                "longName": "Unknown f81c",
                "shortName": "?1C",
                "macaddr": "RBeTiPgc",
                "hwModel": "TBEAM",
            },
            "position": {},
            "lastHeard": 1640204888,
        },
        "SN1": {
            "num": 2475227164,
            "user": {
                "id": "SN1",
                "longName": "Unknown f81c",
                "shortName": "UF81",
                "macaddr": "RBeTiPgc",
                "hwModel": "TBEAM",
            },
            "position": {"raw": "bad data"},
            "lastHeard": 1640204888,
        },
    }

    iface.nodesByNum = {1: anode}
    iface.nodes = nodes
    iface.devPath = "COM4"

    myInfo = MagicMock(return_value=nodes["!9388f81c"])
    iface.myInfo = myInfo

    getMyUser = MagicMock(return_value=nodes["!9388f81c"]["user"])
    iface.getMyUser = getMyUser

    # local node
    iface.localNode = MagicMock(autospec=Node)
    mock_canned_message = "canned_plugin_message:test\n'test'"
    iface.localNode.get_canned_message = MagicMock(return_value=mock_canned_message)
    iface.localNode.channels = [
        MagicMock(autospec=Channel),
        MagicMock(autospec=Channel),
        Channel(),
    ]

    app.interface = iface

    # db setup
    app.db = db.Database("test.sqlite")
    with app.db as database:
        database.insert_message(
            1,
            "sender2",
            "!9388f81c",
            "first message",
            1,
            datetime.datetime(year=2022, month=12, day=18).isoformat(),
        )
        database.insert_message(
            1, "sender1", "^all", "testing", 0, datetime.datetime.now().isoformat()
        )
        database.insert_position(
            1,
            "sender1",
            "^all",
            1,
            1,
            1,
            datetime.datetime(year=2022, month=12, day=18).isoformat(),
        )
        database.insert_position(
            2, "SN1", "^all", 1, 1, 1, datetime.datetime.now().isoformat()
        )
    # other setup can go here

    yield app

    # clean up / reset resources here
    os.remove("test.sqlite")


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
