

class TestGetNode:
    def test_existing_node(self, client):
        resp = client.get("/node-info/!9388f81c")
        assert resp.status_code == 200
        assert resp.json["user"]["id"] == "!9388f81c"
    def test_remove_raw(self, client):
        resp = client.get("/node-info/SN1")
        assert resp.status_code == 200
        assert resp.json["position"].get("raw") == None
    def test_non_existant_node(self, client):
        resp = client.get("/node-info/fakeSerial")
        assert resp.status_code == 404


class TestGetAllNodes:
    def test_all_nodes(self, client):
        resp = client.get("/node-info")
        assert resp.status_code == 200
        mockNodes = [
            {
            'num': 2475227164,
            'user': {
                'id': '!9388f81c',
                'longName': 'Unknown f81c',
                'shortName': '?1C',
                'macaddr': 'RBeTiPgc',
                'hwModel': 'TBEAM'
            },
            "deviceMetrics": None,
            'position': {
                "altitude": None,
                "latitude": None,
                "longitude": None,
                "time": None
            },
            'lastHeard': 1640204888,
            'deviceMetrics': {'batteryLevel': None, 'voltage': None, 'channelUtilization': None, 'airUtilTx': None}
        },
        {
            'num': 2475227164,
            'user': {
                'id': 'SN1',
                'longName': 'Unknown f81c',
                'shortName': '?1C',
                'macaddr': 'RBeTiPgc',
                'hwModel': 'TBEAM'
            },
            "deviceMetrics": None,
            'position': {
                "altitude": None,
                "latitude": None,
                "longitude": None,
                "time": None,
            },
            'lastHeard': 1640204888,
            'deviceMetrics': {'batteryLevel': None, 'voltage': None, 'channelUtilization': None, 'airUtilTx': None}
        }
        ]
        print(resp.json)
        assert resp.json == mockNodes