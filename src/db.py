# built in
import sqlite3
import datetime

# 3rd party
import meshtastic.serial_interface
from pubsub import pub

class Database:
    def __init__(self, path):
        self.path = path
        self.connection = None
        self.cursor = None
    def __enter__(self):
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                uuid INTEGER,
                sender INTEGER,
                target INTEGER,
                text TEXT,
                channel INTEGER,
                timestamp TEXT
            );
            """
        )
        return self
    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.connection.commit()
        self.connection.close()
        self.connection = None
        self.cursor = None
    def insert(self, uuid, sender, target, text, channel, timestamp):
        if not self.connection:
            raise RuntimeError('No connection found, please use `with Database("/path") as db:` syntax')
        self.cursor.execute(
            "INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?);",
            [uuid, sender, target, text, channel, timestamp]
        )


def onMessage(packet, interface, db_path="db.sqlite"):
    uuid = packet['id']
    sender = packet['fromId']
    target = packet['toId']
    text = packet['decoded']['payload'].decode()
    channel = packet.get("channel", 0)
    timestamp = datetime.datetime.fromtimestamp(packet['rxTime'])
    timestamp = timestamp.isoformat()
    with Database(db_path) as db:
        db.insert(uuid, sender, target, text, channel, timestamp)


def start():
    """For use in the main app"""
    pub.subscribe(onMessage, "meshtastic.receive.text")

if __name__ == "__main__": # pragma: no cover
    interface = meshtastic.serial_interface.SerialInterface()
    while True:
        pub.subscribe(onMessage, "meshtastic.receive.text")
