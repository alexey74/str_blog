from rest_framework import authentication


class BearerAuthentication(authentication.TokenAuthentication):
    """Token auth class for DRF using Bearer header keyword."""

    keyword = "Bearer"
