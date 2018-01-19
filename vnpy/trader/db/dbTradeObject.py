from mongoengine import *

class TradeObjectHandler(Document):
    task_id = StringField(required=True, max_length=200)
    startegy_name = StringField(required=True, max_length=200)
    riskctrl_name = StringField(required=True, max_length=200)

    stock_nmae = StringField(required=True, max_length=200)
    stock_code =IntField(required=True)
    riskctrl_name =IntField(required=True)
