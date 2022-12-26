class TestPositions:
    def test_get_all(self, client):
        resp = client.get("/positions")
        assert resp.status_code == 200
        assert len(resp.json) == 2

    def test_get_by_node(self, client):
        resp = client.get("/positions/UF81")
        assert resp.status_code == 200
        assert len(resp.json) == 1
        assert resp.json[0]["uuid"] == 2

    def test_get_bad_node(self, client):
        resp = client.get("/positions/nope")
        assert resp.status_code == 404