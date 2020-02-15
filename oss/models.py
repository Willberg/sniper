from mongoengine import Document, FileField, StringField


class OssDoc(Document):
    oss = FileField()
    content_type = StringField()
