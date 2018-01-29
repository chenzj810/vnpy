from mongoengine import Document, StringField, SequenceField

class DBTaskHandler(Document):
    task_id = SequenceField(primary_key=True)
    stock_name = StringField(required=True, max_length=200)
    stock_code = StringField(required=True, max_length=200)


    obj_amount = StringField(required=True, max_length=200)

    strategy_name = StringField(required=True, max_length=200)
    riskctrl_name = StringField(required=True, max_length=200)
    gateway_name = StringField(required=True, max_length=200)
    #trade_gateway = StringField(required=True, max_length=200)

