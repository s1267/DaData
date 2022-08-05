from models import sqlite_db, Config


def get_config():
    with sqlite_db:
        return Config.get_or_none(Config.id == 1)


def update_config(**kwargs):
    with sqlite_db:
        config = get_config()
        if config:
            config.update(**kwargs).where(Config.id == 1).execute()
            return True
        else:
            return False


def create_config(api_key: str, api_secret: str, response_language: str = None, max_notes: int = 10):
    with sqlite_db:
        if get_config():
            return False
        else:
            Config(
                api_key=api_key,
                api_secret=api_secret,
                response_language=response_language or 'ru',
                max_notes=max_notes,
            ).save()
            return True


# print(create_config('ddd','ddd'))
# print(get_config())
# print(update_config(max_notes='dd'))
