# built in
from unittest.mock import MagicMock

# to mock
from meshtastic import __main__ as meshtastic

class TestConfig:
    def test_get_config(self, client):
        meshtastic.export_config = MagicMock(
            return_value="""
# start of Meshtastic configure yaml
channel_url: https://meshtastic.org/e/#CisSIEmJyqAo4UOYKV7QI0yge-nVHsXD9BZy03SUHMHgCNVfGgdTd2Vuc29uEgoIATgBQANIAVAe
config:
  bluetooth:
    enabled: true
    fixedPin: 123456
  device:
    serialEnabled: true
  display:
    screenOnSecs: 600
  lora:
    hopLimit: 3
    region: US
    txEnabled: true
    txPower: 30
    usePreset: true
  network:
    ntpServer: 0.pool.ntp.org
  position:
    gpsAttemptTime: 900
    gpsEnabled: true
    gpsUpdateInterval: 120
    positionBroadcastSecs: 30
    positionBroadcastSmartEnabled: true
    positionFlags: 3
    rxGpio: 34
    txGpio: 12
  power:
    lsSecs: 300
    meshSdsTimeoutSecs: 7200
    minWakeSecs: 10
    sdsSecs: 4294967295
    waitBluetoothSecs: 60
location:
  alt: 100
  lat: 42
  lon: -88
module_config:
  mqtt:
    address: mqtt.meshtastic.org
    password: large4cats
    username: meshdev
  rangeTest:
    sender: 30
  telemetry:
    deviceUpdateInterval: 900
    environmentUpdateInterval: 900
owner: Swenson Node 0
owner_short: SN0
            """ 
        )
        resp = client.get("/localConfig")
        assert resp.status_code == 200
        required_keys = [
            'channel_url',
            'config',
            'location',
            'module_config',
            'owner',
            'owner_short'
        ]
        for key in required_keys:
            assert key in resp.json.keys()

    def test_post_full_config(self, client):
      body = {
        "owner": "Swenson Node 0",
        "owner_short": "SN0",
        "channel_url": "http://meshtastic.org/asdfadsf",
        "location": {
          "alt": 0,
          "lat": 0,
          "lon": 0
        },
        "config": {
          "section": {
            "ignore_incoming": "string",
          }
        },
        "module_config": {
          "section": {
            "ignore_incoming": "string",
          }
        }
      }
      resp = client.post("/localConfig", json=body)
      assert resp.status_code == 200

class TestCannedMessage:
    def test_get_message(self, client):
        resp = client.get("/localConfig/canned-message")
        assert resp.status_code == 200
        assert resp.json == { "canned_message": "test" }

    def test_post_message(self, client):
        body = { "canned_message": "New Test" }
        resp = client.post("/localConfig/canned-message", json=body)
        assert resp.status_code == 200
        assert resp.json == body

    def test_bad_post_message(self, client):
        body = { "fake": "data" }
        resp = client.post("/localConfig/canned-message", json=body)
        assert resp.status_code == 400