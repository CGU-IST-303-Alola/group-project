import pytest
from app import create_app

@pytest.fixture
def client():
	app = create_app()
	app.config["TESTING"] = True
	with app.test_client() as client:
		yield client

@pytest.mark.parametrize("route", ["/home"])
def test_protected_routes(client, route):
	response = client.get(route, follow_redirects=False)
	assert response.status_code == 302
	assert "/login" in response.headers["Location"]