def test_root_route(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.json()['message'] == 'Hi, I am Israel. Awesome - Your setup is done & working.'

