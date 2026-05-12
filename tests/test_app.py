import pytest
import sys
import os

# Make sure Python can find app.py in the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ── Test 1: Home page loads ────────────────────────────────────────────────────
def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200


# ── Test 2: Valid ride request returns 201 and correct fields ──────────────────
def test_request_ride_success(client):
    response = client.post('/request-ride', json={
        "pickup": "Arusha Bus Stand",
        "destination": "Clock Tower",
        "customer": "Kennie"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 'Pending'
    assert data['pickup'] == 'Arusha Bus Stand'
    assert data['destination'] == 'Clock Tower'
    assert data['customer'] == 'Kennie'


# ── Test 3: Missing fields returns 400 ────────────────────────────────────────
def test_request_ride_missing_destination(client):
    response = client.post('/request-ride', json={
        "pickup": "Majengo"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


# ── Test 4: Rider dashboard returns expected keys ─────────────────────────────
def test_rider_dashboard(client):
    response = client.get('/rider-dashboard')
    assert response.status_code == 200
    data = response.get_json()
    assert 'rider' in data
    assert 'assigned_trips' in data
    assert 'earnings_today' in data


# ── Test 5: Trips endpoint returns list ───────────────────────────────────────
def test_get_trips(client):
    response = client.get('/trips')
    assert response.status_code == 200
    data = response.get_json()
    assert 'total' in data
    assert 'trips' in data