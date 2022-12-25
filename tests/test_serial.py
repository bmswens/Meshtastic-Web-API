
class TestPort:
    def test_get_port(self, client):
        resp = client.get("/serialPort")
        assert resp.status_code == 200
        assert resp.json == {"port": "COM4"}