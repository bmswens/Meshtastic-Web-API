
class TestPositions:
    def test_get_all(self, client):
        resp = client.get("/positions")
        assert resp.status_code == 200
        assert len(resp.json) == 1