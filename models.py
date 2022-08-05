import datetime as dt
import os
import traceback

import peewee

PATH_TO_DB = os.path.join(os.path.dirname(__file__), 'database.db')

sqlite_db = peewee.SqliteDatabase(PATH_TO_DB)


class BaseModel(peewee.Model):
    class Meta:
        database = sqlite_db

    created_at = peewee.DateTimeField(default=dt.datetime.now())
    updated_at = peewee.DateTimeField(default=dt.datetime.now())

    def save(self, *args, **kwargs):
        self.updated_at = dt.datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)


class Config(BaseModel):
    api_key = peewee.CharField(unique=True)
    api_secret = peewee.CharField(unique=True)
    response_language = peewee.CharField(default='ru')
    max_notes = peewee.IntegerField(default=10)


try:
    sqlite_db.create_tables([Config])

except Exception as e:
    traceback.print_exc(e)
