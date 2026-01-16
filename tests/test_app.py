"""
Tests for CI/CD Challenge App
==============================
These tests will be run automatically in your CI pipeline!
"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app, add, subtract, multiply, divide


class TestMathFunctions:
    """Test the math utility functions."""

    def test_add(self):
        """Test addition."""
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0, 0) == 0

    def test_subtract(self):
        """Test subtraction."""
        assert subtract(5, 3) == 2
        assert subtract(1, 1) == 0
        assert subtract(0, 5) == -5

    def test_multiply(self):
        """Test multiplication."""
        assert multiply(3, 4) == 12
        assert multiply(0, 100) == 0
        assert multiply(-2, 3) == -6

    def test_divide(self):
        """Test division."""
        assert divide(10, 2) == 5
        assert divide(7, 2) == 3.5
        assert divide(0, 5) == 0

    def test_divide_by_zero(self):
        """Test division by zero raises error."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)


class TestAPI:
    """Test the Flask API endpoints."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_home(self, client):
        """Test home endpoint."""
        response = client.get('/')
        assert response.status_code == 200
        data = response.get_json()
        assert 'app' in data
        assert 'version' in data
        assert 'endpoints' in data

    def test_health(self, client):
        """Test health endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'

    def test_version(self, client):
        """Test version endpoint."""
        response = client.get('/version')
        assert response.status_code == 200
        data = response.get_json()
        assert 'version' in data
        assert 'environment' in data


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_add_large_numbers(self):
        """Test with large numbers."""
        assert add(10**10, 10**10) == 2 * 10**10

    def test_negative_numbers(self):
        """Test with negative numbers."""
        assert add(-5, -3) == -8
        assert multiply(-2, -3) == 6
        assert divide(-10, 2) == -5

    def test_float_division(self):
        """Test division returns float."""
        result = divide(5, 2)
        assert isinstance(result, float)
        assert result == 2.5
