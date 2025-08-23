"""AuthX configuration"""
import os

from authx import AuthX, AuthXConfig

from config import db_settings


authx_config = AuthXConfig()
authx_config.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
authx_config.JWT_TOKEN_LOCATION=['headers']
authx_config.JWT_HEADER_NAME = "Authorization"
authx_config.JWT_HEADER_TYPE = "Bearer"
authx_config.JWT_ACCESS_TOKEN_EXPIRES = None


authx = AuthX(
    config=authx_config
)


