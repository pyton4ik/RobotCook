from sqlalchemy.orm import sessionmaker

from errors import ReceiptNotFound
from models import engine
from models import Receipt


class ReceiptControll:
    def __init__(self):
        Session = sessionmaker()
        Session.configure(bind=engine)
        self.session = Session()

    @staticmethod
    def get_dict_from_query(query_res: Receipt):
        ret_val = {}
        for attr_name in [x for x in dir(query_res.first()) if not x.startswith('__')]:
            ret_val[attr_name] = getattr(query_res, attr_name)

        return ret_val

    def get_receipt_dict_from_db(self, product_id: int):
        query_res = self.session.query(Receipt).filter_by(product_id=product_id)

        if not query_res.exists():
            raise ReceiptNotFound()

        return map(ReceiptControll.get_dict_from_query, query_res)

class PaymentControll:
    pass

