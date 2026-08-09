import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Config:
    # Database Config
    DB_SERVER = os.getenv("DB_SERVER", "localhost")
    DB_NAME = os.getenv("DB_NAME", "JLR")
    DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
    DB_TRUSTED_CONNECTION = os.getenv("DB_TRUSTED_CONNECTION", "yes").lower()
    DB_USER = os.getenv("DB_USER", "")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

    # LLM Config
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
    OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", 0.0))

    @classmethod
    def get_db_uri(cls) -> str:
        """Constructs the SQLAlchemy MS SQL Server connection string."""
        # URL encode the driver spaces for SQLAlchemy
        driver_param = cls.DB_DRIVER.replace(" ", "+")

        if cls.DB_TRUSTED_CONNECTION == "yes":
            return (
                f"mssql+pyodbc://@{cls.DB_SERVER}/{cls.DB_NAME}"
                f"?driver={driver_param}&trusted_connection=yes"
            )
        else:
            return (
                f"mssql+pyodbc://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_SERVER}/{cls.DB_NAME}"
                f"?driver={driver_param}"
            )

# Instantiate single config object
config = Config()