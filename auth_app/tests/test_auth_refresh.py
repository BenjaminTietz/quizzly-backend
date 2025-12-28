def test_login_sets_cookies(api_client, user):
    response = api_client.post(
        "/api/login/",
        {
            "username": "testuser",
            "password": "Testpass123",
        },
        format="json",
    )

    assert response.status_code == 200
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies

def test_access_token_allows_authenticated_request(api_client, user):
    login = api_client.post(
        "/api/login/",
        {
            "username": "testuser",
            "password": "Testpass123",
        },
        format="json",
    )

    api_client.cookies = login.cookies

    response = api_client.get("/api/quizzes/")

    assert response.status_code == 200
