import os

from fastapi import Response


class CookieManager:
    ACCESS_TOKEN_MAX_AGE = 60 * 30
    REFRESH_TOKEN_MAX_AGE = 60 * 60 * 24 * 7
    DOMAIN = os.getenv("COOKIE_DOMAIN", None)
    SECURE = os.getenv("COOKIE_SECURE", "False").lower() == "true"

    @classmethod
    def set_login_cookies(cls, response: Response, access_token: str, refresh_token: str):
        response.set_cookie(
            key="accessToken",
            value=access_token,
            httponly=True,
            secure=cls.SECURE,
            max_age=cls.ACCESS_TOKEN_MAX_AGE,
            samesite="strict",
            domain=cls.DOMAIN
        )

        response.set_cookie(
            key="refreshToken",
            value=refresh_token,
            httponly=True,
            secure=cls.SECURE,
            max_age=cls.REFRESH_TOKEN_MAX_AGE,
            samesite="strict",
            domain=cls.DOMAIN,
            path="/auth/reissue"
        )

    @classmethod
    def clear_login_cookies(cls, response: Response):
        response.delete_cookie(key="accessToken", domain=cls.DOMAIN)
        response.delete_cookie(key="refreshToken", domain=cls.DOMAIN)
