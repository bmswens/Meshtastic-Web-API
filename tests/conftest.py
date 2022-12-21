# built in
import os

# 3rd party
from meshtastic.serial_interface import SerialInterface
from meshtastic.mesh_interface import MeshInterface
from meshtastic.node import Node
import pytest

# custom
# add to os.sys.path so that we don't have to make a package
this_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(this_dir), 'src')
os.sys.path.append(src_dir)
from app import create_app

class MockInterface(MeshInterface):
    def __init__(self, super):
        print('am fake')
        super.__init__()


@pytest.fixture()
def app():
    # mock SerialInterface to always return a MeshInterface whithout 
    # trying to connect over serial
    SerialInterface.__init__ = lambda x: None

    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # mock out the meshtastic interface
    mockNodes = {
        "serialNumber": {
            "user": {"id": "001", "shortName": "SN0"},
            "position": {}
        },
        "otherSerial": {
            "user": {"id": "002", "shortName": "SN1"},
            "position": {"raw": "testing value"}
        }
    }
    app.interface.nodes = mockNodes
    

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
