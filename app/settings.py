from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = 'localhost'
    server_port: int = 8006
    is_debug: bool = True


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
