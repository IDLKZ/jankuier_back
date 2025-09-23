from datetime import date, timedelta
from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

# Загружаем данные с .env
load_dotenv()


class AppConfiguration(BaseSettings):
    # App Basic Settings
    app_name: str = Field(default="Сервис лицензирования ФКК", env="APP_NAME")
    app_description: str = Field(
        default="Сервис лицензирования ФКК", env="APP_DESCRIPTION"
    )
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    app_debug: bool = Field(default=False, env="APP_DEBUG")
    app_starter_page_url: str | None = Field(default="/", env="APP_STARTER_PAGE_URL")
    app_docs_url: str | None = Field(default=False, env="APP_DOCS_URL")
    app_redoc_url: str | None = Field(default=False, env="APP_REDOC_URL")
    app_status: str = Field(default="development", env="APP_STATUS")
    app_administrator_docs_url: str = Field(
        default="administrator", env="APP_ADMINISTRATOR_DOCS_URL"
    )
    app_client_docs_url: str = Field(default="club", env="APP_CLIENT_DOCS_URL")
    # CORS MIDDLEWARE
    app_cors_enabled: bool = Field(default=False, env="APP_CORS_ENABLED")
    cors_allowed_origins: list[str] = Field(default=["*"], env="CORS_ALLOWED_ORIGINS")
    cors_allow_credentials: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")
    cors_allowed_methods: list[str] = Field(default=["*"], env="CORS_ALLOWED_METHODS")
    cors_allowed_headers: list[str] = Field(default=["*"], env="CORS_ALLOWED_HEADERS")
    # Authentication
    app_auth_type: str = Field(..., env="APP_AUTH_TYPE")
    # Database Choice: 'postgresql' or 'mysql'
    app_database: str | None = Field(default="postgresql", env="APP_DATABASE")
    # Devops
    app_host: str | None = Field(default="localhost", env="APP_HOST")
    app_port: int | None = Field(default=8000, env="APP_PORT")
    # Database Settings
    db_pool_size: int = Field(..., env="DB_POOL_SIZE")
    db_max_overflow: int = Field(..., env="DB_MAX_OVERFLOW")
    db_pool_timeout: int = Field(..., env="DB_POOL_TIMEOUT")
    db_pool_recycle: int = Field(..., env="DB_POOL_RECYCLE")
    # My SQL
    mysql_connection: str = Field(default="mysql+aiomysql", env="MYSQL_CONNECTION")
    mysql_timezone: str = Field(default="+05:00", env="MYSQL_TIMEZONE")
    mysql_db_host: str = Field(default="localhost", env="MYSQL_DB_HOST")
    mysql_db_port: int = Field(default=5432, env="MYSQL_DB_PORT")
    mysql_db_user: str = Field(default="postgres", env="MYSQL_DB_USER")
    mysql_db_password: str = Field(default="root", env="MYSQL_DB_PASSWORD")
    mysql_db_name: str = Field(default="digital_queue", env="MYSQL_DB_NAME")
    # PostgreSQL specific settings
    pg_connection: str = Field(default="postgresql+asyncpg", env="PG_CONNECTION")
    pg_timezone: str = Field(default="Asia/Almaty", env="PG_TIMEZONE")
    pg_db_host: str = Field(default="localhost", env="PG_DB_HOST")
    pg_db_port: int = Field(default=5432, env="PG_DB_PORT")
    pg_db_user: str = Field(default="postgres", env="PG_DB_USER")
    pg_db_password: str = Field(default="root", env="PG_DB_PASSWORD")
    pg_db_name: str = Field(default="digital_queue", env="PG_DB_NAME")
    # File Settings
    static_folder: str | None = Field(default="static", env="STATIC_FOLDER")
    upload_folder: str | None = Field(default="upload", env="UPLOAD_FOLDER")
    template: str | None = Field(default="templates", env="TEMPLATE")
    app_upload_max_file_size_mb: int | None = Field(
        default=100, env="APP_UPLOAD_MAX_FILE_SIZE_MB"
    )
    not_allowed_extensions: list[str] | None = Field(
        default={}, env="NOT_ALLOWED_EXTENSIONS"
    )
    # nosec
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(..., env="ALGORITHM")
    access_token_expire_minutes: int = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(..., env="REFRESH_TOKEN_EXPIRE_DAYS")
    # Logging
    logger_filepath: str = Field(default=..., env="LOGGER_FILEPATH")
    logger_stdout: bool = Field(default=True, env="LOGGER_STDOUT")
    logger_level: str = Field(default="INFO", env="LOGGER_LEVEL")
    logger_serializer: bool = Field(default=False, env="LOGGER_SERIALIZER")
    logger_colorize: bool = Field(default=True, env="LOGGER_COLORIZE")
    logger_enqueue: bool = Field(default=True, env="LOGGER_ENQUEUE")
    logger_backtrace: bool = Field(default=True, env="LOGGER_BACKTRACE")
    logger_diagnose: bool = Field(default=False, env="LOGGER_DIAGNOSE")

    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_password: str | None = Field(default=None, env="REDIS_PASSWORD")
    redis_db: int = Field(default=0, env="REDIS_DB")

    # SOTA Auth
    sota_auth_api: str = Field(default="https://sota.id/api/auth/token/", env="SOTA_AUTH_API")
    sota_auth_email: str = Field(..., env="SOTA_AUTH_EMAIL")
    sota_auth_password: str = Field(..., env="SOTA_AUTH_PASSWORD")
    sota_token_save_minutes: int = Field(default=60, env="SOTA_TOKEN_SAVE_MINUTES")

    # SOTA Registers
    sota_get_country_api: str = Field(default="https://sota.id/api/registers/countries/", env="SOTA_GET_COUNTRY_API")
    sota_get_sports_api: str = Field(default="https://sota.id/api/registers/sports/", env="SOTA_GET_SPORTS_API")

    # Ticketon
    ticketon_get_cities: str = Field(default="https://api.ticketon.kz/get_cities", env="TICKETON_GET_CITIES")
    ticketon_get_shows: str = Field(..., env="TICKETON_GET_SHOWS")
    ticketon_get_show: str = Field(..., env="TICKETON_GET_SHOW")
    ticketon_show_level: str = Field(..., env="TICKETON_SHOW_LEVEL")
    ticketon_get_level: str = Field(..., env="TICKETON_GET_LEVEL")
    ticketon_create_sale: str = Field(..., env="TICKETON_CREATE_SALE")
    ticketon_sale_confirm: str = Field(..., env="TICKETON_SALE_CONFIRM")
    ticketon_sale_cancel: str = Field(..., env="TICKETON_SALE_CANCEL")
    ticketon_sale_refund: str = Field(..., env="TICKETON_SALE_REFUND")
    ticketon_order_check: str = Field(..., env="TICKETON_ORDER_CHECK")
    ticketon_ticket_check: str = Field(..., env="TICKETON_TICKET_CHECK")
    ticketon_update_redis_in_minutes: int = Field(60, env="TICKETON_UPDATE_REDIS_IN_MINUTES")
    ticketon_api_key:str = Field(...,env="TICKETON_API_KEY")
    ticketon_backref:str = Field(...,env="TICKETON_BACKREF")

    # ALATAU
    terminal_id: str = Field(..., env="TERMINAL_ID")
    merchant_id: str = Field(..., env="MERCHANT_ID")
    shared_secret: str = Field(..., env="SHARED_SECRET")
    alatau_payment_refund_post_url: str = Field(..., env="ALATAU_PAYMENT_REFUND_POST_URL")
    alatau_payment_status_post_url: str = Field(..., env="ALATAU_PAYMENT_STATUS_POST_URL")

    # SMS Service Configuration
    use_sms_service: bool = Field(default=True, env="USE_SMS_SERVICE")
    fake_sms_code: str = Field(default="5544", env="FAKE_SMS_CODE")
    sms_code_expire_minutes: int = Field(default=2, env="SMS_CODE_EXPIRE_MINUTES")

    # SMSC SMS Service Configuration
    smsc_login: str = Field(default="", env="SMSC_LOGIN")
    smsc_password: str = Field(default="", env="SMSC_PASSWORD")
    smsc_post: bool = Field(default=False, env="SMSC_POST")
    smsc_https: bool = Field(default=False, env="SMSC_HTTPS")
    smsc_charset: str = Field(default="utf-8", env="SMSC_CHARSET")
    smsc_debug: bool = Field(default=False, env="SMSC_DEBUG")

    # SMTP Configuration for SMS
    smtp_from: str = Field(default="api@smsc.kz", env="SMTP_FROM")
    smtp_server: str = Field(default="send.smsc.kz", env="SMTP_SERVER")
    smtp_login: str = Field(default="", env="SMTP_LOGIN")
    smtp_password: str = Field(default="", env="SMTP_PASSWORD")

    @property
    def get_connection_url(self) -> str:
        """Get the connection URL for the chosen database."""
        if self.app_database == "postgresql":
            return f"{self.pg_connection}://{self.pg_db_user}:{self.pg_db_password}@{self.pg_db_host}:{self.pg_db_port}/{self.pg_db_name}"
        if self.app_database == "mysql":
            return f"{self.mysql_connection}://{self.mysql_db_user}:{self.mysql_db_password}@{self.mysql_db_host}:{self.mysql_db_port}/{self.mysql_db_name}"
        get_connection_err_msg = "Неверная строка подключения"
        raise ValueError(get_connection_err_msg)

    def get_connection_sync_url(self) -> str:
        """Get the connection URL for the chosen database (synchronous)."""
        if self.app_database == "postgresql":
            # Используем синхронный драйвер psycopg2
            return (
                f"postgresql+psycopg2://{self.pg_db_user}:{self.pg_db_password}"
                f"@{self.pg_db_host}:{self.pg_db_port}/{self.pg_db_name}"
            )

        if self.app_database == "mysql":
            # Используем синхронный драйвер pymysql
            return (
                f"mysql+pymysql://{self.mysql_db_user}:{self.mysql_db_password}"
                f"@{self.mysql_db_host}:{self.mysql_db_port}/{self.mysql_db_name}"
            )

    @field_validator("app_status")
    def validate_app_status(cls, v: str | None):  # noqa:ANN201
        if v.lower() not in {"development", "production"}:
            validate_app_status_err_msg = (
                "APP_STATUS должен быть 'development' или 'production'"
            )
            raise ValueError(validate_app_status_err_msg)
        return v

    @field_validator("app_auth_type")
    def validate_app_auth_type(cls, v: str | None):  # noqa:ANN201
        if v.lower() not in {"local", "keycloak"}:
            validate_app_auth_type_err_msg = (
                "APP_AUTH_TYPE должен быть 'local' или 'keycloak'"
            )
            raise ValueError(validate_app_auth_type_err_msg)
        return v

    def is_keycloak_auth(self) -> bool:
        return self.app_auth_type.lower() == "keycloak"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


app_config = AppConfiguration()
