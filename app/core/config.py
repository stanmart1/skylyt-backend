from pydantic_settings import BaseSettings
from pydantic import Field, AliasChoices, model_validator
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # Redis/Dragonfly (accepts common production env var names)
    DRAGONFLY_URL: str = Field(
        default="redis://localhost:6379/0",
        validation_alias=AliasChoices(
            "DRAGONFLY_URL",
            "REDIS_URL",
            "REDIS_URI",
            "REDIS_PRIVATE_URL",
            "REDISCLOUD_URL",
            "UPSTASH_REDIS_URL",
        ),
    )

    # Optional granular Redis settings (used if a full URL is not provided)
    REDIS_HOST: Optional[str] = None
    REDIS_PORT: Optional[int] = None
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: Optional[int] = None
    REDIS_USERNAME: Optional[str] = None

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Email
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    FROM_EMAIL: str = "noreply@skylytluxury.com"
    
    # Frontend URL
    FRONTEND_URL: str = "https://skylyt.scaleitpro.com"

    # Comma-separated list of allowed CORS origins (optional).
    # When unset, the defaults in main.py are used.
    CORS_ORIGINS: Optional[str] = None
    
    # External APIs
    STRIPE_SECRET_KEY: Optional[str] = None
    
    # Flutterwave
    FLUTTERWAVE_SECRET_KEY: Optional[str] = None
    FLUTTERWAVE_PUBLIC_KEY: Optional[str] = None
    
    # Paystack
    PAYSTACK_SECRET_KEY: Optional[str] = None
    PAYSTACK_PUBLIC_KEY: Optional[str] = None
    
    # PayPal
    PAYPAL_CLIENT_ID: Optional[str] = None
    PAYPAL_CLIENT_SECRET: Optional[str] = None
    PAYPAL_SANDBOX: bool = True
    
    # Travel APIs
    BOOKING_COM_API_KEY: Optional[str] = None
    EXPEDIA_API_KEY: Optional[str] = None
    HERTZ_API_KEY: Optional[str] = None
    
    # Environment
    ENVIRONMENT: str = "production"
    DEBUG: bool = False

    # Resend Email API
    RESEND_API_KEY: Optional[str] = None

    # Exchange Rate API
    EXCHANGE_RATE_API_KEY: Optional[str] = None

    @model_validator(mode="after")
    def _build_redis_url_from_parts(self):
        """Allow configuring Redis via individual REDIS_* variables."""
        url = self.DRAGONFLY_URL or ""
        is_default = url.strip() == "" or "localhost" in url or url == "redis://localhost:6379/0"
        if self.REDIS_HOST and is_default:
            host = self.REDIS_HOST
            port = self.REDIS_PORT or 6379
            db = self.REDIS_DB if self.REDIS_DB is not None else 0
            user = self.REDIS_USERNAME
            password = self.REDIS_PASSWORD
            auth = ""
            if user or password:
                auth = f"{user or ''}:{password or ''}@"
            scheme = "rediss" if str(port) == "6380" else "redis"
            self.DRAGONFLY_URL = f"{scheme}://{auth}{host}:{port}/{db}"
        return self

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()