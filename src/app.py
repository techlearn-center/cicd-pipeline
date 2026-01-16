"""
Simple Flask API for CI/CD Challenge
=====================================
This is a basic Flask app that you'll set up CI/CD for.
"""

import os
from flask import Flask, jsonify

app = Flask(__name__)

# Configuration
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


@app.route("/")
def home():
    """Home endpoint."""
    return jsonify({
        "app": "CI/CD Challenge App",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "message": "Hello from the CI/CD pipeline!",
        "endpoints": {
            "/": "This page",
            "/health": "Health check",
            "/version": "Version info"
        }
    })


@app.route("/health")
def health():
    """Health check endpoint for deployment verification."""
    return jsonify({
        "status": "healthy",
        "version": APP_VERSION
    })


@app.route("/version")
def version():
    """Version endpoint for deployment tracking."""
    return jsonify({
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "commit": os.getenv("GIT_COMMIT", "unknown")
    })


def add(a: int, b: int) -> int:
    """Add two numbers. Used for testing."""
    return a + b


def subtract(a: int, b: int) -> int:
    """Subtract two numbers. Used for testing."""
    return a - b


def multiply(a: int, b: int) -> int:
    """Multiply two numbers. Used for testing."""
    return a * b


def divide(a: int, b: int) -> float:
    """Divide two numbers. Used for testing."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = ENVIRONMENT == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
