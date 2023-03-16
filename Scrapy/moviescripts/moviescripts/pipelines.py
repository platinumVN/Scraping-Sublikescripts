# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo
import sqlite3

############################
# Load environment variables
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = f'{Path(__file__).resolve().parents[4]}' + '\private_env.env'
load_dotenv(dotenv_path=dotenv_path)
CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING')

##############
# Define class
# class MoviescriptsPipeline:
#     def open_spider(self, spider):
#         logging.warning('Spider Opened - Pipeline')
#     def close_spider(self, spider):
#         logging.warning('Spider Closed - Pipeline')
#     def process_item(self, item, spider):
#         return item

class SQLitePipeline:

    def open_spider(self, spider):
        # create database file
        self.connection = sqlite3.connect('transcripts.db')
        # we need a cursor object to execute SQL queries
        self.c = self.connection.cursor()
        #  try/except will help when running this for the +2nd time (we can't create the same table twice)
        try:
            # query: create table with columns
            self.c.execute('''
                CREATE TABLE transcripts(
                    title TEXT,
                    plot TEXT,
                    transcript TEXT,
                    url TEXT
                )
            ''')
            # save changes
            self.connection.commit()
        except sqlite3.OperationalError:
            pass


    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        # query: insert data into table
        self.c.execute('''
            INSERT INTO transcripts (title,plot,transcript,url) VALUES(?,?,?,?)
        ''', (
            item.get('title'),
            item.get('plot'),
            item.get('script'),
            item.get('url'),
        ))
        # save changes
        self.connection.commit()
        return item

class MongodbPipeline:
    """MongoDB
    """
    collection_name = 'transcripts'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(CONNECTION_STRING)
        self.db = self.client['subslikescript']
    def close_spider(self, spider):
        self.client.close()
        logging.warning('MongoClient Closed - Pipeline')
    def process_item(self, item, spider):
        logging.warning('Add item - MongoDB Pipeline')
        self.db[self.collection_name].insert_one(item)
        return item