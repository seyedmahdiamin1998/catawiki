# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from sqlalchemy import create_engine, inspect, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database


class CatawikiPipeline:
    
    def __init__(self):
        self.USER = 'postgres'
        self.PASSWORD = '1234'
        self.DATABASE_NAME = 'catawiki'
        self.SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://{0}:{1}@localhost:5432/{2}".\
            format(self.USER, self.PASSWORD, self.DATABASE_NAME)
        
        self.create_myDatabase()
        self.create_connection()
        self.seller = self.create_table_Sellers()
        self.specification = self.create_table_Specifications()
        self.feedback = self.create_table_Feedbacks()
        self.product = self.create_table_Products()

    def create_myDatabase(self):
        '''
        Create a database to collect data there and if it exists don't do anything.
        '''
        is_database_exists = database_exists(self.SQLALCHEMY_DATABASE_URL)
        if not is_database_exists:
            engine = create_engine(self.SQLALCHEMY_DATABASE_URL)
            create_database(engine.url)
            engine.dispose()

    def create_connection(self):
        '''
        Make connections here to use very where :)
        '''
        self.engine = create_engine(self.SQLALCHEMY_DATABASE_URL, echo=False)
        self.Base = declarative_base()

        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    ######################################################################
    # Products
    def create_table_Products(self):
        '''
        Create a table to collect catawiki's data in there.
        '''
        class Products(self.Base):
            __tablename__ = 'products'
            id = Column(Integer, primary_key=True)
            lotId = Column(Integer, nullable=True)
            category = Column(String(200), nullable=False)
            lotTitle = Column(String(50), nullable=True)
            lotSubtitle = Column(String(50), nullable=True)
            description = Column(String(50), nullable=True)
            
            seller_id = Column(Integer, ForeignKey('sellers.id'), nullable=False)

            auctionId = Column(Integer, nullable=True)

            expertsEstimate_min_EUR = Column(Integer, nullable=True)
            expertsEstimate_min_USD = Column(Integer, nullable=True)
            expertsEstimate_min_GBP = Column(Integer, nullable=True)
            expertsEstimate_max_EUR = Column(Integer, nullable=True)
            expertsEstimate_max_USD = Column(Integer, nullable=True)
            expertsEstimate_max_GBP = Column(Integer, nullable=True)

            favoriteCount = Column(Integer, nullable=True)

        if not inspect(self.engine).has_table(self.DATABASE_NAME):
            self.Base.metadata.create_all(self.engine)

        return Products
    
    def store_product(self, item):
        new_record = self.product(
            lotId = item['lotId'],
            category = item['category'][:200],
            lotTitle = item['lotTitle'][:50],
            lotSubtitle = item['lotSubtitle'][:50],
            description = item['description'][:50],
            seller_id = item['seller_id'],
            auctionId = item['auctionId'],

            expertsEstimate_min_EUR = item['expertsEstimate_min_EUR'],
            expertsEstimate_min_USD = item['expertsEstimate_min_USD'],
            expertsEstimate_min_GBP = item['expertsEstimate_min_GBP'],
            expertsEstimate_max_EUR = item['expertsEstimate_max_EUR'],
            expertsEstimate_max_USD = item['expertsEstimate_max_USD'],
            expertsEstimate_max_GBP = item['expertsEstimate_max_GBP'],
            favoriteCount = item['favoriteCount'])

        self.session.add(new_record)
        self.session.commit()
    ######################################################################
    # Sellers
    def create_table_Sellers(self):
        '''
        Create a table to collect catawiki's Sellers data.
        '''
        class Sellers(self.Base):
            __tablename__ = 'sellers'
            id = Column(Integer, primary_key=True)
            username = Column(String(50), nullable=True)
            country = Column(String(50), nullable=True)
            city = Column(String(50), nullable=True)
            state = Column(String(50), nullable=True)
            zipcode = Column(String(50), nullable=True)
            isPro = Column(Boolean, nullable=True)
            isTop = Column(Boolean, nullable=True)
            createdAt = Column(String(30), nullable=True)
            url = Column(String(200), nullable=True)

            products = relationship('Products', backref='product')
        
        self.Base.metadata.create_all(self.engine)

        return Sellers


    def store_seller(self, item):
        new_record = self.seller(   
            id = item['id'],
            username = item['username'],
            country = item['country'],
            city = item['city'],
            state = item['state'],
            zipcode = item['zipcode'],
            isPro = item['isPro'],
            isTop = item['isTop'],
            createdAt = item['createdAt'],
            url = item['url'])

        self.session.add(new_record)
        self.session.commit()    
    ######################################################################
    # Specifications
    def create_table_Specifications(self):
        '''
        Create a table to collect Specification's items in there.
        '''
        class Specification(self.Base):
            __tablename__ = 'specifications'
            id = Column(Integer, primary_key=True)
            lotId = Column(Integer, nullable=False)
            name = Column(String(200), nullable=True)
            value = Column(String(1000), nullable=True)

            # products = relationship('Products', backref='product')
        
        self.Base.metadata.create_all(self.engine)

        return Specification


    def store_specification(self, item):
        new_record = self.specification(   
            lotId = item['lotId'],
            name = item['name'],
            value = item['value'])

        self.session.add(new_record)
        self.session.commit()  

    ######################################################################
    # Feedbacks
    def create_table_Feedbacks(self):
        '''
        Create a table to collect items feedbacks in there.
        '''
        class Feedback(self.Base):
            __tablename__ = 'feedbacks'
            id = Column(Integer, primary_key=True)
            lotId = Column(Integer, nullable=False)
            type = Column(String(50), nullable = True)
            authorName = Column(String(200), nullable = True)
            body = Column(String(2000), nullable = True)
            locale = Column(String(50), nullable = True)
            createdAt = Column(String(50), nullable = True)
        
        self.Base.metadata.create_all(self.engine)

        return Feedback


    def store_feedback(self, item):
        new_record = self.feedback(   
            lotId = item['lotId'],
            type = item['type'],
            authorName = item['authorName'],
            body = item['body'],
            locale = item['locale'],
            createdAt = item['createdAt'])

        self.session.add(new_record)
        self.session.commit()  
    
    ######################################################################
    def process_item(self, item, spider):
        if not self.session.query(self.seller).filter(self.seller.id==item['seller_info']['id']).first():
            self.store_seller(item['seller_info'])
        
        
        if not self.session.query(self.specification).filter(self.specification.lotId==item['specification_info']['specification_id']).first():
            for record in item['specification_info']['specification_items']: 
                self.store_specification(record)

        if not self.session.query(self.feedback).filter(self.feedback.lotId==item['feedbacks_info']['feeedback_id']).first():
            for record in item['feedbacks_info']['feedbacks_items']: 
                self.store_feedback(record)

        if not self.session.query(self.product).filter(self.product.lotId==item['Product_info']['lotId']).first():
            self.store_product(item['Product_info'])
        
        
        
