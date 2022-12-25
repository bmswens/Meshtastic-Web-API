
class TestSendText:
    def test_bad_message(self, client):
        body = {
            "fake": "data"
        }
        resp = client.post("/messages", json=body)
        assert resp.status_code == 400


    def test_channeless_send(self, client):
        body = {
            "text": "testing"
        }
        resp = client.post("/messages", json=body)
        assert resp.status_code == 200

    def test_bad_channel_send(self, client):
        body = {
            "text": "testing",
            "channelIndex": 100
        }
        resp = client.post("/messages", json=body)
        assert resp.status_code == 400

    def test_unconfig_channel_send(self, client):
        body = {
            "text": "testing",
            "channelIndex": 2
        }
        resp = client.post("/messages", json=body)
        assert resp.status_code == 404

    def test_channel_send(self, client):
        body = {
            "text": "testing",
            "channelIndex": 1
        }
        resp = client.post("/messages", json=body)
        assert resp.status_code == 200


class TestGetText:
    def test_get_all(self, client):
        resp = client.get("/messages")
        assert resp.status_code == 200
        assert len(resp.json) == 2
    def test_get_by_dm(self, client):
        resp = client.get("/messages?dm=true")
        assert resp.status_code == 200
        assert len(resp.json) == 1
        assert resp.json[0]["text"] == "first message"
    def test_get_messages_limit(self, client):
        resp = client.get("/messages?limit=1")
        assert resp.status_code == 200
        assert len(resp.json) == 1
        assert resp.json[0]["text"] == "testing"