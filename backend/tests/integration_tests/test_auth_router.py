def test_sign_up_and_sign_in(client):
    response = client.post(
        "/api/v1/auth/sign-up",
        json={"email": "new@test.com", "password": "test", "name": "test"},
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["email"] == "new@test.com"
    assert response_json["name"] == "test"
    assert isinstance(response_json["id"], str)

    response = client.post(
        "/api/v1/auth/sign-in",
        json={"email": "new@test.com", "password": "test"},
    )

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["user_info"]["email"] == "new@test.com"
    assert response_json["user_info"]["name"] == "test"
    assert isinstance(response_json["user_info"]["id"], str)
    assert response_json["access_token"] is not None
