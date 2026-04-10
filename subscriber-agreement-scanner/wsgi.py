"""WSGI entry point for production deployment."""

from bastion_scan.web import create_app

app = create_app()
