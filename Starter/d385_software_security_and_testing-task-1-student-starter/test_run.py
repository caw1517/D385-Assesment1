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

def test_invalid_equipment_type_handled(client, caplog):
    caplog.set_level(logging.INFO)
    response = client.post('/rent', data={
        'equipment_type': 'SpaceShuttle',  # Invalid equipment
        'days': '3'
    })
    assert response.status_code == 200, \
        "Invalid equipment type caused a crash! Implement try/except."

    assert b"Please select a valid equipment type." in response.data
    assert b"Rental Confirmation" not in response.data
    assert b"Total Cost:" not in response.data

    errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
    msg = next((m for m in errors if "unknown equipment" in m), None)
    assert msg is not None, "No unknown-equipment ERROR was logged"
    assert "SpaceShuttle" in msg

    infos = [r.getMessage() for r in caplog.records if r.levelno == logging.INFO]
    assert not any("rental calculated" in m for m in infos)


def test_non_numeric_days_handled(client, caplog):
    caplog.set_level(logging.INFO)

    response = client.post('/rent', data={
        'equipment_type': 'Bulldozer',
        'days': 'abc'  # Invalid - not a number
    })

    assert response.status_code == 200, \
        "Non-numeric days caused a crash! Implement try/except."

    assert b"Please enter a whole number of rental days." in response.data
    assert b"Rental Confirmation" not in response.data
    assert b"Total Cost:" not in response.data

    warnings = [r.getMessage() for r in caplog.records if r.levelno == logging.WARNING]
    msg = next((m for m in warnings if "invalid rental duration" in m), None)
    assert msg is not None, "No invalid-duration WARNING was logged"
    assert "abc" in msg

    infos = [r.getMessage() for r in caplog.records if r.levelno == logging.INFO]
    assert not any("rental calculated" in m for m in infos)


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
    """Only usernames on the allowed list pass validation."""
    for name in ["admin", "alice", "bob", "charlie"]:
        assert validate_username(name) is True, f"{name} should be allowed"

    assert validate_username("hacker") is False
    assert validate_username("") is False
    assert validate_username("Admin") is False


# ------------------------------------------------------------
# REQUIRED TEST 2: Correct Output Test
# Write a test that verifies a function returns the expected value.
# Example: Test rental calculation returns correct totals
# ------------------------------------------------------------

def test_student_correct_output(client):
    """Each piece of equipment shows the correct rental total."""
    cases = [
        ("Bulldozer", "3", b"Total Cost: $1500"),
        ("Excavator", "5", b"Total Cost: $2250"),
        ("Crane", "1", b"Total Cost: $800"), 
    ]
    for equipment, days, expected in cases:
        response = client.post("/rent", data={"equipment_type": equipment, "days": days})

        assert response.status_code == 200
        assert b"Rental Confirmation" in response.data, f"{equipment}: no confirmation shown"
        assert expected in response.data, f"{equipment} x {days} days: wrong total"


# ------------------------------------------------------------
# REQUIRED TEST 3: Application Behavior Test
# Write a test that verifies the application behaves correctly.
# Example: Test login, route accessibility, or error messages
# ------------------------------------------------------------

def test_student_application_behavior(client, caplog):
    """A valid login redirects home, greets the user, and logs an INFO event."""
    caplog.set_level(logging.INFO)
    creds = {"username": "admin", "password": "secret123"}

    response = client.post("/login", data=creds, follow_redirects=False)
    assert response.status_code == 302

    response = client.post("/login", data=creds, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/"
    assert b"Welcome back, admin!" in response.data
    assert b"Invalid credentials." not in response.data

    infos = [r.getMessage() for r in caplog.records if r.levelno == logging.INFO]
    msg = next((m for m in infos if "successful login" in m), None)
    assert msg is not None, "No successful-login INFO was logged"
    assert "admin" in msg
    assert "secret123" not in msg



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