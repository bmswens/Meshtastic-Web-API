class TestSendMessage:
    def test_no_text(self, client):
        body = {
            "user_name": "bmswens",
            "token": "XYZ"
        }
        resp = client.post('/mattermost', json=body)
        assert resp.status_code == 400
    def test_no_token(self, client):
        body = {
            "user_name": "bmswens",
            "text": "123"
        }
        resp = client.post('/mattermost', json=body)
        assert resp.status_code == 403
    def test_full_send(self, client):
        body = {
            "user_name": "bmswens",
            "token": "XYZ",
            "text": "123"
        }
        resp = client.post('/mattermost', json=body)
        assert resp.status_code == 200
