# built in
import os
import sqlite3
import datetime

# 3rd party
import meshtastic.serial_interface
from pubsub import pub

# custom
from api.mattermost import onMessage as mmOnMessage


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


class Database:
    def __init__(self, path):
        self.path = path
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                uuid INTEGER,
                sender TEXT,
                target TEXT,
                text TEXT,
                channel INTEGER,
                timestamp TEXT
            );
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS positions (
                uuid INTEGER,
                sender TEXT,
                target TEXT,
                altitude INTEGER,
                longitude REAL,
                latitude REAL,
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

    def insert_message(self, uuid, sender, target, text, channel, timestamp):
        if not self.connection:
            raise RuntimeError(
                'No connection found, please use `with Database("/path") as db:` syntax'
            )
        self.cursor.execute(
            "INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?);",
            [uuid, sender, target, text, channel, timestamp],
        )

    def get_messages(self, limit=None, dm=None):
        if not self.connection:
            raise RuntimeError(
                'No connection found, please use `with Database("/path") as db:` syntax'
            )
        results = None
        if not limit and not dm:
            results = self.cursor.execute(
                "SELECT * FROM messages ORDER BY timestamp DESC;"
            )
        elif limit:
            results = self.cursor.execute(
                "SELECT * FROM messages ORDER BY timestamp DESC LIMIT ?;", [limit]
            )
        elif dm:
            results = self.cursor.execute(
                "SELECT * FROM messages WHERE target=? ORDER BY timestamp DESC;", [dm]
            )
        return [row for row in results]

    def insert_position(
        self, uuid, sender, target, altitude, latitude, longitude, timestamp
    ):
        if not self.connection:
            raise RuntimeError(
                'No connection found, please use `with Database("/path") as db:` syntax'
            )
        self.cursor.execute(
            "INSERT INTO positions VALUES (?, ?, ?, ?, ?, ?, ?);",
            [uuid, sender, target, altitude, latitude, longitude, timestamp],
        )

    def get_positions(self, node=None, limit=None):
        if not self.connection:
            raise RuntimeError(
                'No connection found, please use `with Database("/path") as db:` syntax'
            )

        query = "SELECT * FROM positions ORDER BY timestamp DESC;"
        args = []
        if node:
            query = "SELECT * FROM positions WHERE sender = ? ORDER BY timestamp DESC;"
            args.append(node)
        results = self.cursor.execute(
            query,
            args
        ) 
        return [row for row in results]


def onMessage(packet, interface, db_path=None):
    if not db_path:  # pragma: no cover
        db_path = get_db_path()
    uuid = packet["id"]
    sender = packet["fromId"]
    target = packet["toId"]
    text = packet["decoded"]["payload"].decode()
    channel = packet.get("channel", 0)
    timestamp = datetime.datetime.now()
    rxTime = packet.get("rxTime")
    if rxTime:
        timestamp = datetime.datetime.fromtimestamp(rxTime)
        timestamp = timestamp.isoformat()
    with Database(db_path) as db:
        db.insert_message(uuid, sender, target, text, channel, timestamp)

    # mattermost integration
    mattermost_url = os.getenv("MATTERMOST_WEBHOOK")
    if mattermost_url:
        mmOnMessage(packet, interface)


def onPosition(packet, interface, db_path=None):
    if not db_path:  # pragma: no cover
        db_path = get_db_path()
    uuid = packet["id"]
    sender = packet["fromId"]
    target = packet["toId"]
    position = packet["decoded"]["position"]
    altitude = position["altitude"]
    longitude = position["longitude"]
    latitude = position["latitude"]
    timestamp = datetime.datetime.fromtimestamp(packet["rxTime"])
    timestamp = timestamp.isoformat()
    with Database(db_path) as db:
        db.insert_position(
            uuid, sender, target, altitude, latitude, longitude, timestamp
        )


def get_db_path():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(this_dir), "data")
    os.makedirs(data_dir, exist_ok=True)
    db_path = os.path.join(data_dir, "db.sqlite")
    return db_path


def start():
    """For use in the main app"""
    pub.subscribe(onMessage, "meshtastic.receive.text")
    pub.subscribe(onPosition, "meshtastic.receive.position")
    return get_db_path()


if __name__ == "__main__":  # pragma: no cover
    interface = meshtastic.serial_interface.SerialInterface()
    while True:
        pub.subscribe(onMessage, "meshtastic.receive.text")
        pub.subscribe(onPosition, "meshtastic.receive.position")
