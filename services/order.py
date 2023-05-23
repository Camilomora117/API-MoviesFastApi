from schemas.order import Order, OrderMovie
from models.order import Order as OrderModel
from models.order import OrderMovie as OrderMovieModel
from schemas.movie import Movie, MovieCreated
from models.movie import Movie as MovieModel

class OrderService():
    
    def __init__(self, db) -> None:
        self.db = db

    def get_orders(self):
        result = self.db.query(OrderModel).all()
        return result
    
    def create_order(self, movie: Order):
        new_order = OrderModel(**movie.dict())
        self.db.add(new_order)
        self.db.commit()
        return new_order
    
    def get_order_by_Id(self, id):
        result = self.db.query(OrderModel).filter(OrderModel.id == id).first()
        return result

    def update_order(self, id: int, data: Order):
        order = self.db.query(OrderModel).filter(OrderModel.id == id).first()
        order.user_id = data.user_id
        self.db.commit()
        return
    
    def delete_order(self, id: int):
       self.db.query(OrderModel).filter(OrderModel.id == id).delete()
       self.db.commit()
       return
    
    #OrderMovie
    def create_order_movie(self, order_movie: OrderMovie):
        new_order_movie = OrderMovieModel(**order_movie.dict())
        self.db.add(new_order_movie)
        self.db.commit()
        return new_order_movie
    
    def get_order_movies_by_id(self, id_order):
        result = self.db.query(OrderMovieModel).filter(OrderMovieModel.order_id == id_order).all()
        list_result = []
        if not result:
            return [] 
        for i in result:
            movie = self.db.query(MovieModel).filter(MovieModel.id == i.movie_id).first()
            movie_created = MovieCreated(
                id=movie.id, 
                title=movie.title, 
                overview=movie.overview,
                year=movie.year,
                rating=movie.rating,
                category=movie.category,
                quantity=i.quantity
                )
            list_result.append(movie_created)
        return list_result
    
    def delete_movies_of_order(self, id_order):
        self.db.query(OrderMovieModel).filter(OrderMovieModel.order_id == id_order).delete()
        self.db.commit()
        return





