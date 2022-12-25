# built in
import os
import datetime

# 3rd party
from pubsub import pub
import pytest

# custom
# add to os.sys.path so that we don't have to make a package
this_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(this_dir), 'src')
os.sys.path.append(src_dir)
import db

class TestDB:
    def test_bad_connect(self):
        d = db.Database(":memory:")
        with pytest.raises(RuntimeError):
            d.insert_message(1, 1, 2, "test", 0, datetime.datetime.now().isoformat())
        with pytest.raises(RuntimeError):
            d.get_messages()
        with pytest.raises(RuntimeError):
            d.get_positions()
        with pytest.raises(RuntimeError):
            d.insert_position(1, 1, 1, 1, 1, 1, datetime.datetime.now().isoformat())

    def test_insert_message(self):
        with db.Database(":memory:") as d:
            d.insert_message(1, 1, 2, "test", 0, datetime.datetime.now().isoformat())
    def test_insert_position(self):
        with db.Database(":memory:") as d:
            d.insert_position(1, 1, 1, 1, 1, 1, datetime.datetime.now().isoformat())
    def test_rec_msg(self):
        # TODO: Figure out how to test this better
        db.start()
        packet = {
            "id": 1,
            "fromId": 1,
            "toId": 2,
            "decoded": {
                "payload": b'test'
            },
            "rxTime": 2
        }
        db.onMessage(packet, {}, ":memory:")

    def test_rec_position(self):
        packet = {
            "id": 1,
            "fromId": 1,
            "toId": 2,
            "decoded": {
                "position": {
                    "altitude": 0,
                    "latitude": 0,
                    "longitude": 0
                }
            },
            "rxTime": 3
        }
        db.onPosition(packet, {}, ":memory:")