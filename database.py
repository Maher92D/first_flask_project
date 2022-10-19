import sqlite3
import pandas as pd

class database:

    def __init__(self, dbpath):

        self.conn = sqlite3.connect(dbpath, check_same_thread=False)

    def sql_create_table(self, tablename, values, types=None):
        c = self.conn.cursor()
        query = f'''CREATE TABLE IF NOT EXISTS {tablename} (id INTEGER PRIMARY KEY '''
        for value in values:
            query += f",[{value}] text"
        query += ")"
        c.execute(query)

    def sql_get_column_names(self, tablename):
        c = self.conn.cursor()
        c.execute(f'''SELECT * FROM {tablename} ''')
        return [i[0] for i in c.description]

    def sql_get_all(self, tablename):
        c = self.conn.cursor()
        c.execute(f'''SELECT * FROM {tablename} ''')
        return c.fetchall()

    def removelast(self, string):
        return string.rstrip(string[-1])

    def sql_insert(self, tablename, values):
        column_names = self.sql_get_column_names(tablename)
        del column_names[0]
        query = f'''INSERT OR IGNORE INTO {tablename}('''
        for column in column_names:
            query += f"{column},"
        query = self.removelast(query)
        query += f")"

        query += f"VALUES ("
        for value in values:
            query += f"?,"
        query = self.removelast(query)
        query += ")"

        c = self.conn.cursor()
        c.execute(query, values)

    def sql_update_by_id(self, tablename, values, id):
        column_names = self.sql_get_column_names(tablename)
        del column_names[0]
        query = f'''UPDATE {tablename} SET '''
        for column, value in zip(column_names, values):
            query += f"{column}= ?,"
        query = self.removelast(query)
        query += f" WHERE id = ?"

        values.append(id)
        c = self.conn.cursor()
        print(query)
        c.execute(query, values)

    def sqlquery(self, query):
        c = self.conn.cursor()
        c.execute(query)
        result = c.fetchall()
        return result

    def sql_delete_by_id(self, table_name, id):

        query = f"DELETE FROM {table_name} WHERE id=={id};"
        c = self.conn.cursor()
        print(query)
        c.execute(query)

    def sql_select_by_id(self, table_name, id):
        query = f"SELECT * FROM {table_name} WHERE id=={id};"
        c = self.conn.cursor()
        c.execute(query)
        result = c.fetchall()
        return result

    def sql_select_by_column(self, table_name, column, value):
        query = f"SELECT * FROM {table_name} WHERE {column}=={value};"
        c = self.conn.cursor()
        c.execute(query)
        result = c.fetchall()
        return result

    def get_tablelist(self):
        c = self.conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        result = c.fetchall()
        return result

    def get_DataFrame(self,query):
        c = self.conn.cursor()
        c.execute(query)
        columns = [i[0] for i in c.description]
        result = c.fetchall()
        df = pd.DataFrame(result, columns=columns)
        print(df)
        return df

    def commit(self):
        self.conn.commit()

if __name__ == '__main__':

    db = database("db")
    print(db.sql_get_all("mytable"))
    db.get_DataFrame("SELECT * FROM mytable")