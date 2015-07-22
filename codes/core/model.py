#coding = utf-8
from mongoengine import connect,Document,EmbeddedDocument,EmbeddedDocumentField,EmailField,StringField,DateTimeField,IntField,FloatField,FileField\
                        ,BooleanField,ListField,ReferenceField,LongField,CASCADE,DENY,NULLIFY
import setting
import time

connect(db=setting.db['name'])

class Temperature(EmbeddedDocument):
    temperature = FloatField(default=0)
    makeTime = FloatField(default=time.time())

class Humidity(EmbeddedDocument):
    humidity = FloatField(default=0)
    makeTime = FloatField(default=time.time())

class Device(Document):
    deviceId = StringField(max_length=20,primary_key=True)

    temperatures = ListField(EmbeddedDocumentField(Temperature))
    humiditys = ListField(EmbeddedDocumentField(Humidity))

    coAlert = BooleanField(default=False)
    chAlert = BooleanField(default=False)
    guardAlert = BooleanField(default=False)

    lastTime = FloatField(default=time.time())


class User(Document):
    name = StringField(max_length=20,unique=True,required=True)
    dev = ReferenceField(Device)
    password = StringField(max_length=40,required=True)
    type = StringField(max_length=20,default='user')


