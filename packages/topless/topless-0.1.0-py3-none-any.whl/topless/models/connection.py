import json
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker


class ConnectionCredentialError(RuntimeError):
    pass


class Connection:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(
        self,
        user: str = None,
        endpoint: str = None,
        port: int = None,
        name: str = None,
        secret_arn: str = None,
        password: str = None,
    ) -> None:
        self._session = None
        self._engine = None
        self.user = user or os.environ.get("DB_USER")
        self.endpoint = endpoint or os.environ.get("DB_ENDPOINT")
        self.port = port or os.environ.get("DB_PORT", "5432")
        self.name = name or os.environ.get("DB_NAME")
        self.secret_arn = secret_arn or os.environ.get("DB_SECRET_ARN", None)
        self.password = password or os.environ.get("DB_PASSWORD", None)
        self.region = os.environ.get("AWS_REGION")
        self.environment = os.environ.get("ENVIRONMENT", "development")
        self.is_development = self.environment == "development"

        if not (self.user and self.endpoint and self.name and self.port):
            raise ConnectionCredentialError("Invalid database credentials.")

        if not self.secret_arn and not self.is_development:
            raise ConnectionCredentialError(
                "You must provide DB_SECRET_ARN environment variable."
            )

        if not self.password and not self.is_development:
            raise ConnectionCredentialError(
                "You must provide DB_PASSWORD or DB_SECRET_ARN environment variable."
            )

    @property
    def session(self) -> Session:
        if self._session:
            return self._session

        self._session = self.create_session()
        return self._session

    def create_session(self) -> Session:
        session_factory = sessionmaker(
            bind=self._get_engine(), future=True, expire_on_commit=False
        )
        session: Session = scoped_session(session_factory)
        return session

    def get_connection_string(self):
        password = None

        if self.is_development and self.password:
            password = self.password
        else:
            password = self.get_secret_password()

        conn = "postgresql+pg8000://{}:{}@{}:{}/{}".format(
            self.user, password, self.endpoint, self.port, self.name
        )

        return conn

    def get_secret_password(self):
        # secret = get_secret(self.secret_arn)

        # password = json.loads(secret).get("password")
        password = "234"

        return password

    def _get_engine(self):
        if self._engine:
            return self._engine

        self._engine = create_engine(self.get_connection_string())

        return self._engine
