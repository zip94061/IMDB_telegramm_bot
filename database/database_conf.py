from os import path

from peewee import SqliteDatabase, Model, IntegerField, DateTimeField, TextField


db = SqliteDatabase(path.join('database', 'database.db'))


class History(Model):
    user_id = IntegerField()
    user_name = TextField()
    date = DateTimeField()
    requests = TextField()

    class Meta:
        database = db


def create_database():
    db.create_tables([History])
    db.close()
