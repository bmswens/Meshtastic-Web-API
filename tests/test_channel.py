
class TestSendText:
    def test_bad_message(self, client):
        body = {
            "fake": "data"
        }
        resp = client.post("/channel/message", json=body)
        assert resp.status_code == 400


    def test_channeless_send(self, client):
        body = {
            "text": "testing"
        }
        resp = client.post("/channel/message", json=body)
        assert resp.status_code == 200

    def test_bad_channel_send(self, client):
        body = {
            "text": "testing",
            "channelIndex": 100
        }
        resp = client.post("/channel/message", json=body)
        assert resp.status_code == 400

    def test_unconfig_channel_send(self, client):
        body = {
            "text": "testing",
            "channelIndex": 2
        }
        resp = client.post("/channel/message", json=body)
        assert resp.status_code == 404

    def test_channel_send(self, client):
        body = {
            "text": "testing",
            "channelIndex": 1
        }
        resp = client.post("/channel/message", json=body)
        assert resp.status_code == 200


