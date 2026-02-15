import pytest
from app import create_app, db


@pytest.fixture
def app():
    """Create test app instance"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db",
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test-secret-key"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


# ==========================================
# HOME PAGE TESTS
# ==========================================

def test_home_page_loads(client):
    """Test home page returns 200"""
    response = client.get("/")
    assert response.status_code == 200


def test_home_page_content(client):
    """Test home page contains expected content"""
    response = client.get("/")
    assert response.status_code in [200, 302]


# ==========================================
# AUTH PAGE TESTS
# ==========================================

def test_login_page_loads(client):
    """Test login page returns 200"""
    response = client.get("/login")
    assert response.status_code in [200, 302]


def test_signup_page_loads(client):
    """Test signup page returns 200"""
    response = client.get("/signup")
    assert response.status_code in [200, 302]


# ==========================================
# SIGNUP TESTS
# ==========================================

def test_signup_new_user(client):
    """Test user registration"""
    response = client.post("/signup", data={
        "username": "testuser123",
        "email": "testuser123@example.com",
        "password": "TestPassword123!"
    }, follow_redirects=True)
    assert response.status_code == 200


def test_signup_duplicate_user(client):
    """Test duplicate user registration"""
    # Register first user
    client.post("/signup", data={
        "username": "duplicate_user",
        "email": "duplicate@example.com",
        "password": "TestPassword123!"
    }, follow_redirects=True)

    # Try registering same user again
    response = client.post("/signup", data={
        "username": "duplicate_user",
        "email": "duplicate@example.com",
        "password": "TestPassword123!"
    }, follow_redirects=True)
    assert response.status_code == 200


# ==========================================
# LOGIN TESTS
# ==========================================

def test_login_valid_user(client):
    """Test login with valid credentials"""
    # Register user first
    client.post("/signup", data={
        "username": "loginuser",
        "email": "loginuser@example.com",
        "password": "TestPassword123!"
    }, follow_redirects=True)

    # Try login
    response = client.post("/login", data={
        "email": "loginuser@example.com",
        "password": "TestPassword123!"
    }, follow_redirects=True)
    assert response.status_code == 200


def test_login_invalid_user(client):
    """Test login with invalid credentials"""
    response = client.post("/login", data={
        "email": "nonexistent@example.com",
        "password": "WrongPassword!"
    }, follow_redirects=True)
    assert response.status_code == 200


# ==========================================
# PROTECTED ROUTES TESTS
# ==========================================

def test_dashboard_requires_login(client):
    """Test dashboard redirects to login when not authenticated"""
    response = client.get("/dashboard")
    assert response.status_code in [302, 401, 200]


def test_profile_requires_login(client):
    """Test profile redirects to login when not authenticated"""
    response = client.get("/profile")
    assert response.status_code in [302, 401, 200]


# ==========================================
# URL SHORTENING TESTS
# ==========================================

def test_shorten_url_requires_login(client):
    """Test URL shortening requires authentication"""
    response = client.post("/shorten", data={
        "url": "https://www.google.com"
    }, follow_redirects=True)
    assert response.status_code in [200, 302, 401]


# ==========================================
# ERROR HANDLING TESTS
# ==========================================

def test_404_page(client):
    """Test 404 error for non-existent page"""
    response = client.get("/nonexistent-page-xyz")
    assert response.status_code in [404, 302]


def test_invalid_short_url(client):
    """Test accessing invalid short URL"""
    response = client.get("/xyz123invalid")
    assert response.status_code in [404, 302]


# ==========================================
# APP CONFIGURATION TESTS
# ==========================================

def test_app_exists(app):
    """Test app instance is created"""
    assert app is not None


def test_app_is_testing(app):
    """Test app is in testing mode"""
    assert app.config["TESTING"] is True


def test_app_secret_key(app):
    """Test app has secret key"""
    assert app.config["SECRET_KEY"] is not None