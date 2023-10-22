"""Configuration for application"""
from core.config._main import AppConfig
from core.config.swagger import get_swagger_config

__all__ = ["AppConfig", "get_swagger_config"]
