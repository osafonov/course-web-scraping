# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime

import sqlite3


class SqLitePipline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect('immobilien.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """
                create table if not exists sources (
                    id integer primary key,
                    name text unique,
                    url text
                )
            """
        )
        self.cursor.execute(
            """
                create table if not exists companies (
                    id integer primary key,
                    name text unique,
                    address text,
                    phone text,
                    email text,
                    contact_person text
                )
            """
        )
        self.cursor.execute(
            """
                create table if not exists adverts (
                    id integer primary key,
                    source_id integer,
                    company_id integer,
                    origin_id text,
                    url text unique,
                    title text,
                    address text,
                    price float,
                    rooms integer,
                    size float,
                    floor integer,
                    full_text text,
                    date timestamp,
                    created_at timestamp
                )
            """
        )
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute(
            """
                insert or ignore into sources (name, url) values (?, ?) 
            """, (item['source']['name'], item['source']['url'])
        )
        self.cursor.execute("select id from sources where name=?", (item['source']['name'],))
        row = self.cursor.fetchone()
        (source_id, ) = row if row else None

        self.cursor.execute(
            """
                insert or ignore into companies (name) values (?)
            """, (item['company']['name'],)
        )
        row = self.cursor.execute("select id from companies where name=?", (item['company']['name'],)).fetchone()
        (company_id, ) = row if row else None

        self.cursor.execute(
            """
                insert or ignore into adverts (source_id, company_id, origin_id, url, title, address, price, rooms, floor, size, full_text, date, created_at) 
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                source_id, company_id,
                item['ad']['id'], item['ad']['url'], item['ad']['title'], item['ad']['address'], item['ad']['price'],
                item['ad']['rooms'], item['ad']['floor'], item['ad']['size'], item['ad']['full_text'], item['ad']['date'],
                datetime.now())
        )
        self.connection.commit()
        return item