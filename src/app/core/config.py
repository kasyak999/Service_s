from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки подключения к базе данных."""

    app_title: str = 'Service_s'

    postgres_user: str = 'user'
    postgres_password: str = 'mysecretpassword'
    postgres_db: str = 'django'
    postgres_port: str = '5433'
    secret: str = 'SECRET'
    debug: bool = True
    server_public_ip: str = '127.0.0.1'
    publickey: str = 'PUBLICKEY'

    @property
    def database_url(self) -> str:
        """Формирует URL подключения к базе."""
        db_host = f'localhost:{self.postgres_port}' if self.debug else 'db'
        return (
            'postgresql+asyncpg://'
            f'{self.postgres_user}:{self.postgres_password}@{db_host}'
            f'/{self.postgres_db}'
        )

    class Config:
        env_file = '.env'


settings = Settings()
