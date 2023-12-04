from pathlib import Path
from typing import Any, Dict, Optional

import tomli

DEFAULT_HANDLER_CONFIG: Dict[str, Any] = {
    "runtime": "python3.11",
    "timeout": 120,
    "memory": 256,
    "tracing": "Active",
}

DEFAULT_API_CONFIG: Dict[str, str] = {
    "cors_allow_origin": "cors_allow_origin",
    "cors_allow_headers": "'Content-Type, Authorization'",
}


class Singleton(type):
    _instances: Dict = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=Singleton):
    """
    Singleton Configuration class to load and access configuration data.
    """

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path("config.toml")
        self.config_data = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found at {self.config_path}"
            )
        with open(self.config_path, "rb") as f:
            return tomli.load(f)

    @property
    def app_name(self) -> Optional[str]:
        return self.config_data.get("app", {}).get("name")

    @property
    def app_slug(self) -> Optional[str]:
        return self.config_data.get("app", {}).get("slug")

    @property
    def handlers(self) -> Dict[str, Any]:
        return self.config_data.get("handlers", DEFAULT_HANDLER_CONFIG)

    @property
    def api(self) -> Dict[str, str]:
        return self.config_data.get("api", DEFAULT_API_CONFIG)
