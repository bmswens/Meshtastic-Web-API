

class TestGetNode:
    def test_existing_node(self, client):
        resp = client.get("/nodes/info/SN0")
        assert resp.status_code == 200
        assert resp.json["user"]["id"] == "001"
    def test_remove_raw(self, client):
        resp = client.get("/nodes/info/SN1")
        assert resp.status_code == 200
        assert resp.json["position"].get("raw") == None
    def test_non_existant_node(self, client):
        resp = client.get("/nodes/info/fakeSerial")
        assert resp.status_code == 404


class TestGetAllNodes:
    def test_all_nodes(self, client):
        resp = client.get("/nodes/all")
        assert resp.status_code == 200
        assert "serialNumber" in resp.json
        assert "otherSerial" in resp.json
        assert len(resp.json) == 2
    def test_all_nodes_detailed(self, client):
        resp = client.get("/nodes/all?detailed=true")
        assert resp.status_code == 200
        mockNodes = {
            "serialNumber": {
                "user": {"id": "001", "shortName": "SN0"},
                "position": {}
            },
            "otherSerial": {
                "user": {"id": "002", "shortName": "SN1"},
                "position": {}
            }
        }
        assert resp.json == mockNodes