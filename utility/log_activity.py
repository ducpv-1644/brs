from datetime import datetime

from django.conf import settings
import pymongo

from components.users.models import User
from components.books.models import Book


class ActivityLog(object):
    LIMIT = 20

    # activity
    FAVORITE_MSG = 'have liked the book '
    UNFAVORITE_MSG = 'have unliked the book '
    READING = 'are reading to page '
    READ = 'have finished the book '
    FOLLOW = 'followed the user'
    UNFLLOW = 'unfollowed the user'
    COMMENT = ''

    def __init__(self):
        self.host = settings.MONGO_LOG.get('HOST')
        self.port = settings.MONGO_LOG.get('PORT')
        self.client = pymongo.MongoClient(f'mongodb://{self.host}:{self.port}/')
        self.db = self.client[settings.MONGO_LOG.get('NAME')]
        self.book_col = self.db['activity']

    def log_activity(self, source_user: User, obj_target, activity):
        data = {
            'source_user': source_user.username,
            'source_user_id': source_user.id,
            'activity': activity,
            'create_at': datetime.now()
        }
        if isinstance(obj_target, Book):
            data.update({'obj_target_name': obj_target.name, 'obj_target_id': obj_target.id, 'obj_target': 'book'})
        if isinstance(obj_target, User):
            data.update({'obj_target_name': obj_target.username, 'obj_target_id': obj_target.id, 'obj_target': 'user'})
        self.book_col.insert_one(data)

    def get_activity_log(self, user: User, limit: int):
        data_book = self.book_col.find({
            'source_user': user.username,
            'source_user_id': user.id
        }).sort("create_at", -1).limit(limit)

        return data_book
