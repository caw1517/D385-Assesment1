"""
WGU Construction Equipment Rental - Test Suite

This test file has TWO sections:

SECTION 1: Pre-written Validation Tests (PROVIDED)
    These tests verify your security fixes are working. Run them to confirm
    your defensive coding implementations plugged the vulnerabilities.

SECTION 2: Student-Created Tests (YOU MUST COMPLETE)
    You must create 3 additional test cases using assertion statements.
    This satisfies Rubric Aspect A7: "The learner creates unit tests that
    use assertion statements to confirm code behaves as expected."

How to Run:
    pytest test_run.py -v

Expected Results:
- BEFORE your fixes: Some tests will FAIL (vulnerabilities exist)
- AFTER your fixes:  All tests should PASS
"""

import pytest
import logging
from app_student import app, validate_username, EQUIPMENT_PRICES, verify_equipment_catalog


# ------------------------------------------------------------
# Test Fixture
# Creates a test client for making requests to your Flask app
# ------------------------------------------------------------

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ============================================================
#              SECTION 1: PROVIDED VALIDATION TESTS
#           (These verify your security fixes work)
# ============================================================

# --- Exception Handling Tests ---
# These will FAIL until you implement try/except blocks

def test_invalid_equipment_type_handled(client):
    """
    Test that invalid equipment types don't crash the app.
    FAILS if you haven't implemented try/except for KeyError.
    """
    response = client.post('/rent', data={
        'equipment_type': 'SpaceShuttle',  # Invalid equipment
        'days': '3'
    })
    assert response.status_code == 200, \
        "Invalid equipment type caused a crash! Implement try/except."


def test_non_numeric_days_handled(client):
    """
    Test that non-numeric days input doesn't crash the app.
    FAILS if you haven't implemented try/except for ValueError.
    """
    response = client.post('/rent', data={
        'equipment_type': 'Bulldozer',
        'days': 'abc'  # Invalid - not a number
    })
    assert response.status_code == 200, \
        "Non-numeric days caused a crash! Implement try/except."


@pytest.mark.parametrize("days", ["0", "-5"])
def test_nonpositive_days_rejected(client, days):
    response = client.post(
        "/rent",
        data={"equipment_type": "Bulldozer", "days": days},
    )

    assert response.status_code == 200
    assert b"Rental duration must be greater than 0" in response.data
    assert b"Rental Confirmation" not in response.data
    assert b"Total Cost:" not in response.data


# ============================================================
#              SECTION 2: STUDENT-CREATED TESTS
#         (You must complete these to satisfy Aspect A7)
# ============================================================

# ------------------------------------------------------------
# REQUIRED TEST 1: Input Validation Test
# Write a test that validates input is checked correctly.
# Example: Test the validate_username function
# ------------------------------------------------------------

def test_student_input_validation():
    """
    TODO: Write assertions to test input validation.

    Requirements:
    - Use assert statements to verify expected behavior
    - Test at least 2 different scenarios

    Example ideas:
    - Test that valid usernames (admin, alice, bob, charlie) return True
    - Test that invalid usernames return False
    - Test that the EQUIPMENT_PRICES dictionary contains expected values

    Hint:
        assert validate_username("admin") == True
        assert validate_username("hacker") == False
    """
    # TODO: Write your assertions below (remove the pass statement)
    pass


# ------------------------------------------------------------
# REQUIRED TEST 2: Correct Output Test
# Write a test that verifies a function returns the expected value.
# Example: Test rental calculation returns correct totals
# ------------------------------------------------------------

def test_student_correct_output(client):
    """
    TODO: Write assertions to verify correct function outputs.

    Requirements:
    - Use assert statements to verify expected behavior
    - Test at least 1 calculation or output

    Example ideas:
    - Bulldozer ($500/day) for 3 days should show $1500
    - Excavator ($450/day) for 5 days should show $2250
    - Crane ($800/day) for 2 days should show $1600

    Hint:
        response = client.post('/rent', data={
            'equipment_type': 'Bulldozer',
            'days': '3'
        })
        assert response.status_code == 200
        assert b'1500' in response.data
    """
    # TODO: Write your assertions below (remove the pass statement)
    pass


# ------------------------------------------------------------
# REQUIRED TEST 3: Application Behavior Test
# Write a test that verifies the application behaves correctly.
# Example: Test login, route accessibility, or error messages
# ------------------------------------------------------------

def test_student_application_behavior(client):
    """
    TODO: Write assertions to verify application behavior.

    Requirements:
    - Use assert statements to verify expected behavior
    - Test at least 1 application feature

    Example ideas:
    - Test that the home page returns status code 200
    - Test that valid login credentials redirect (status 302)
    - Test that invalid login shows "Invalid credentials" message
    - Test that zero days are handled appropriately

    Hint:
        response = client.get('/')
        assert response.status_code == 200

        response = client.post('/login', data={
            'username': 'admin',
            'password': 'secret123'
        }, follow_redirects=False)
        assert response.status_code == 302  # Redirect on success
    """
    # TODO: Write your assertions below (remove the pass statement)
    pass


# ============================================================
#              OPTIONAL: Additional Tests
#    Add more tests here if you want extra validation
# ============================================================
def test_failed_login_rejected_and_logged(client, caplog):
    caplog.set_level(logging.WARNING)
    response = client.post(
        "/login",
        data={"username": "hacker", "password": "wrongpass"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid credentials." in response.data
    assert b"Welcome back" not in response.data

    warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
    msg = next((r.getMessage() for r in warnings if "failed login" in r.getMessage()), None)
    assert msg is not None, "No failed-login WARNING was logged"
    assert "hacker" in msg
    assert "ip=127.0.0.1" in msg
    assert "wrongpass" not in msg


def test_equipment_catalog_assertions_pass(caplog):
    caplog.set_level(logging.INFO)

    verify_equipment_catalog(EQUIPMENT_PRICES)

    messages = [r.getMessage() for r in caplog.records if r.levelno == logging.INFO]
    assert any("catalog is not empty" in m for m in messages)
    assert any("every daily rate is numeric and > 0" in m for m in messages)