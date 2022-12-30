import sqlite3
from sqlite3 import Error



class Database:
    def __init__(self,path):
        sql_create_items_table = """CREATE TABLE IF NOT EXISTS item (
                                        id integer PRIMARY KEY,
                                        price real NOT NULL,
                                        is_offer boolean NOT NULL,
                                        name text NOT NULL
                                    );"""

        # create a database connection
        self.conn = self.create_connection(path)

        # create tables
        if self.conn is not None:
            # create projects table
            self.create_table(sql_create_items_table)
        else:
            print("Error! cannot create the database connection.")


    def create_connection(self,db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            return self.conn
        except Error as e:
            print(e)

        return self.conn


    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def create_item(self,item):
        """
        Create a new project into the projects table
        :param item:
        :return: item id
        """
        sql = f''' UPDATE item SET 
                    name = '{item['name']}',
                    price = {item['price']},
                    is_offer = '{item['is_offer']}'
                WHERE id = {item['id']} '''

        print('SQL IS', sql)
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        return cur.lastrowid


    def add_item(self,item):
        """
        Create a new project into the projects table
        :param item:
        :return: item id
        """
        sql = f''' INSERT INTO item(name,price,is_offer)
                VALUES('{item['name']}',{item['price']},'{item['is_offer']}') '''
        print('SQL IS', sql)
        cur = self.conn.cursor()
        cur.execute(sql, item)
        self.conn.commit()
        return cur.lastrowid

    def all_items(self):
        sql = ''' SELECT * FROM item '''
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        items = [{
            'id' : r[0],
            'price' : r[1],
            'is_offer' : True if r[2] == 'TRUE' else False,
            'name' : r[3]
        } for r in rows]
        return items

    def get_item(self,item_id):
        sql = f''' SELECT * FROM item WHERE id={item_id} '''
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        item = {
            
        }
        if len(rows) > 0:
            item = {
                'id' : rows[0][0],
                'price' : rows[0][1],
                'is_offer' : True if rows[0][2] == 'TRUE' else False,
                'name' : rows[0][3]
            }
        return item
