from sqlalchemy import Float, Boolean, String, DateTime, Computed, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from database import Base, engine


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)

    name = Column(String)
    type = Column(String, default="sale")
    active = Column(Boolean, default=True)
    price = Column(Float, default=0.0)

    receipts = relationship("Receipt")
    order_items = relationship("OrderItems")


class Payments(Base):
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True)

    amount = Column(Float, default=0.0)
    ref = Column(String)
    payment_type = Column(String)
    payment_date = Column(DateTime)

    order_id = Column(Integer, ForeignKey('order.id'))


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)

    name = Column(String)
    ref = Column(String)

    client_id = Column(Integer)
    state = Column(String, default="draft")

    order_items = relationship("OrderItems")
    payment_items = relationship("Payments")

    @hybrid_property
    def is_paid(self):
        return self.total_payment >= self.total

    @hybrid_property
    def total_payment(self):
        return sum(payment_item.amount for payment_item in self.payment_items)

    @hybrid_property
    def total(self):
        return sum(order_item.total for order_item in self.order_items)


class OrderItems(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)

    qty = Column(Integer)
    processed_qty = Column(Integer, default=0)
    remaining_qty = Column(Integer, Computed('qty - processed_qty'))

    price = Column(Float, default=0.0)
    total = Column(Float, Computed('qty * price'))

    order_id = Column(Integer, ForeignKey("order.id"))
    product_id = Column(Integer, ForeignKey("product.id"))


class Receipt(Base):
    __tablename__ = 'receipt_items'
    id = Column(Integer, primary_key=True)

    ingredient = Column(String)
    operation = Column(String)
    wait_time = Column(Integer)
    sequence = Column(Integer, default=10)

    product_id = Column(Integer, ForeignKey("product.id"))


Base.metadata.create_all(engine)
