from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy import declarative_base, relationship, sessionmaker

Base = declarative_base()
Session = sessionmaker(bind = create_engine)
session = Session


class Review(Base):

    customer_id = Column(Integer, ForeignKey('customers.id'))
    restaurent_id = Column(Integer,ForeignKey('restaurants.id'))
    star_rating = Column(Integer)

    customer = relationship('Customer', back_populates='reviews')
    restaurant = relationship('Restaurant', back_populates='reviews')

    def customer(self):
        return self.customer
    
    def restaurant(self):
        return self.restaurant
    
class REstaurent(Base):

    reviews = relationship('Review', back_populates='restaurant')

    def reviews(self):
        return self.reviews
    
    def customers(self):
        return [review.customer for review in self.reviews]
    
    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()
    
    def all_reviews(self):
        return [review.full_review() for review in self.reviews]
    
class Customer(Base):

    reviews = relationship('Review', back_populates='customer')

    def reviews(self):
        return self.reviews
    
    def restaurant(self):
        return [review.restaurant for review in self.reviews]
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def favorite_restaurant(self):
        favorite_review = session.query(Review).filter_by(customer_id = self.id).order_by(Review.star_rating.desc()).first()

        if favorite_review:
            return favorite_review.restaurant
    
    def add_review(self, restaurant, rating):
        review = Review(
            customer = self,
            restaurant = restaurant,
            star_rating = rating
        )
        session.add(review)
        session.commit()

    def find_all_by_given_name(cls, name):
        return session.query(cls).filter_by(first_name = name).all()
    
class Review(Base):
    def full_review(self):
        return f'Review for {self.restaurant.name} by {self.customer.full_name()}:{self.star_rating} stars'