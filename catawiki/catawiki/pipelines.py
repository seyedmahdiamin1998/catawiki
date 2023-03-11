# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from sqlalchemy import create_engine, inspect, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
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
        self.car = self.create_table_Products()

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

    def create_table_Products(self):
        '''
        Create a table to collect catawiki's data in there.
        '''
        class Products(self.Base):
            __tablename__ = 'products'
            id = Column(Integer, primary_key=True)
            lotId = Column(Integer, nullable=True)
            lotTitle = Column(String(50), nullable=True)
            lotSubtitle = Column(String(50), nullable=True)
            description = Column(String(50), nullable=True)
            
            # seller_id = Column(Integer, nullable=True)
            # seller_username = Column(Integer, nullable=True)
            # seller_country = Column(String(50), nullable=True)
            # seller_city = Column(String(50), nullable=True)
            # seller_state = Column(String(50), nullable=True)
            # seller_zipcode = Column(String(50), nullable=True)
            # seller_isPro = Column(Boolean, nullable=True)
            # seller_isTop = Column(Boolean, nullable=True)
            # seller_createdAt = Column(String(30), nullable=True)
            # seller_url = Column(String(200), nullable=True)
            
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
        new_record = self.car(lotId = item['lotId'],
                              lotTitle = item['lotTitle'][:50],
                              lotSubtitle = item['lotSubtitle'][:50],
                              description = item['description'][:50],

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


    def process_item(self, item, spider):
        self.store_product(item)
        # return item
