

def test_query_all_robots(test_client):
    response = test_client.get("/api/robots")
    assert response.status_code == 200
