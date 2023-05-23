from config.dabatase import Base
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declared_attr

class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    date_created = Column(Date)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    user = relationship('User', backref='users')


class OrderMovie(Base):

    __tablename__ = "order_movies"

    order_id = Column(Integer, ForeignKey('orders.id', ondelete="CASCADE"), primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id', ondelete="CASCADE"), primary_key=True)
    quantity = Column(Integer)

    order = relationship('Order', backref='orders')
    movie = relationship('Movie', backref='movies')

    @declared_attr
    def __mapper_args__(cls):
        return {
            'primary_key': (cls.order_id, cls.movie_id),
            'concrete': True
        }

