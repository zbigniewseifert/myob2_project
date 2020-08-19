import sqlite3


class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('db/app.db')
        self.create_user_table()
        self.create_file_info_table()


    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create_file_info_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS "Fileinfo" (
          id INTEGER PRIMARY KEY,
          Filename TEXT,
          Filepath TEXT,
          Description TEXT,
          _is_public boolean DEFAULT 0,
          _is_deleted boolean DEFAULT 0,
          CreatedOn Date DEFAULT CURRENT_DATE,
          Votes INTEGER DEFAULT 0,
          UserId INTEGER FOREIGNKEY REFERENCES User(id)
        );
        """

        self.conn.execute(query)

    def create_user_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "User" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Email TEXT,
        CreatedOn Date default CURRENT_DATE
        );
        """
        self.conn.execute(query)


class FileDBModel:
    TABLENAME = "Fileinfo"

    def __init__(self):
        self.conn = sqlite3.connect('db/app.db')
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def get_by_id(self, id):
        where_clause = f"AND id={id}"
        return self.list_items(where_clause)

    def create(self, params):
        print (params)
        query = f'insert into {self.TABLENAME} ' \
                f'(Filename, Filepath, Description, UserId) ' \
                f'values ("{params.get("Filename")}","{params.get("Filepath")}",' \
                f'"{params.get("Description")}",' \
                f'"{params.get("UserId")}")'
        print(query)
        result = self.conn.execute(query)
        return self.get_by_id(result.lastrowid)

    def delete(self, item_id):
        query = f"UPDATE {self.TABLENAME} " \
                f"SET _is_deleted =  {1} " \
                f"WHERE id = {item_id}"
        print (query)
        self.conn.execute(query)
        return self.list_items(where_clause="")

    def update(self, item_id, update_dict):
        set_query = ", ".join([f'{column} = {value}'
                     for column, value in update_dict.items()])

        query = f"UPDATE {self.TABLENAME} " \
                f"SET {set_query} " \
                f"WHERE id = {item_id}"
        self.conn.execute(query)
        return self.get_by_id(item_id)

    def list_items(self, where_clause):
        query = f"SELECT id, Filename, Filepath, Description, CreatedOn, UserId, Votes " \
                f"from {self.TABLENAME} WHERE _is_deleted != {1} " + where_clause
        result_set = self.conn.execute(query).fetchall()
        result = [{column: row[i]
                  for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result


class User:
    #Not used as User specific features are not implemented at the moment
    TABLENAME = "User"

    def create(self, name, email):
        query = f'insert into {self.TABLENAME} ' \
                f'(Name, Email) ' \
                f'values ({name},{email})'
        result = self.conn.execute(query)
        return result