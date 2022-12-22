

class TestGetNode:
    def test_existing_node(self, client):
        resp = client.get("/nodes/info/!9388f81c")
        assert resp.status_code == 200
        assert resp.json["user"]["id"] == "!9388f81c"
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
        assert "!9388f81c" in resp.json
        assert "SN1" in resp.json
        assert len(resp.json) == 2
    def test_all_nodes_detailed(self, client):
        resp = client.get("/nodes/all?detailed=true")
        assert resp.status_code == 200
        mockNodes = {
        '!9388f81c': {
            'num': 2475227164,
            'user': {
                'id': '!9388f81c',
                'longName': 'Unknown f81c',
                'shortName': '?1C',
                'macaddr': 'RBeTiPgc',
                'hwModel': 'TBEAM'
            },
            'position': {},
            'lastHeard': 1640204888
        },
        "SN1": {
            'num': 2475227164,
            'user': {
                'id': 'SN1',
                'longName': 'Unknown f81c',
                'shortName': '?1C',
                'macaddr': 'RBeTiPgc',
                'hwModel': 'TBEAM'
            },
            'position': {},
            'lastHeard': 1640204888
        }
    }
        assert resp.json == mockNodes