import pytest
from app.run import app

@pytest.fixture
def client():
	app.config["TESTING"] = True
	with app.test_client() as client:
		yield client

"""
Tests that restricted pages cannot be accessed until login
"""
def test_redirects_require_login(client):
	protected_routes = ["/home"]
	
	for route in protected_routes:
		response = client.get(route, follow_redirects=False)
		assert response.status_code == 302
		assert "/login" in response.headers["Location"]