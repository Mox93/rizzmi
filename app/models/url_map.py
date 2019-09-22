from common.db import db, ExtendedDocument


class UrlMap(ExtendedDocument):
    """
    This Model maps all functions to their endpoints
    """
    meta = {"collection": "url_map"}

    # TODO decide on the way objects will be stored

    endpoint = db.StringField(required=True, max_length=50, unique=True)
    urls = db.ListField(db.URLField(), required=True, unique=True)
    resource = db.BinaryField(required=True)

    @classmethod
    def find_by_endpoint(cls, endpoint):
        return cls.objects(endpoint=endpoint).first()



