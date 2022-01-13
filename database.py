from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    # Parent products for ingradients
    parent_product_id = relationship("Product")


class Payments(Base):
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True)
    sum = Column(Integer)
    payment_type = Column(String)
    order_id = Column(Integer, ForeignKey('order.id'))


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer)
    order_items = relationship("OrderItems")
    payment_items = relationship("Payments")

    @property
    def is_paid(self):
        return self.total_payment >= self.total

    @property
    def total_payment(self):
        return sum(payment_item.sum for payment_item in self.payment_items)

    @property
    def total(self):
        return sum(order_item.sum for order_item in self.order_items)


class OrderItems(Base):
    __tablename__ = 'order_items'
    order_id = Column(Integer, ForeignKey("order.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    qty = Column(Integer)
    price = Column(Integer)

    @property
    def sum(self):
        return self.qty * self.price

Base.metadata.create_all(engine)