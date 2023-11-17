import mysql.connector


class Database:
    def __init__(self, host, user, password, database_):
        self.host = host
        self.user = user
        self.password = password
        self.database = database_
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(host=self.host,
                                                      user=self.user,
                                                      password=self.password,
                                                      database=self.database)
            print("Connected to MySQL database")
        except mysql.connector.Error as e:
            print("Error connecting to MySQL database:", e)

        if self.connection is None:
            return False
        else:
            return True

    def commit_changes(self):
        self.connection.commit()
        return True

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            print("Disconnected from MySQL database")

    def commit_and_disonnect(self) -> None:
        self.commit_changes()
        self.disconnect()

    def execute_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            print("Error executing query:", e)
            return None

    def insert(self, table_name, table_headers, values):
        # Convert the headers and values lists to tuples
        headers = tuple(table_headers)
        values = tuple(values)

        # Create a string with placeholders for the values
        placeholders = ', '.join(['%s'] * len(headers))

        # Use INSERT INTO statement to insert the values into the table
        sql = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({placeholders})"
        if self.connection is None:
            print('please connect to databse before execution')
        else:
            try:
                cursor = self.connection.cursor()
                cursor.execute(sql, values)
                print('data added')
            except Exception as e:
                print('error caused due to {}'.format(e))

    def eraze_table(self, table_name):
        query = f"TRUNCATE TABLE {table_name}"
        self.execute_query(query)

    def swap_table(self, table_name) -> list:
        query = f"SELECT * FROM {table_name}"
        return self.execute_query(query)
        #return type [ (), () ]

    def fetch_limit(self, table_name, limit) -> list:
        query = f"SELECT * FROM {table_name} LIMIT {limit};"
        try:
            return self.execute_query(query)
        except Exception as E:
            print(E)
            return False

    def fetch_first_row(self, table_name: str) -> tuple:
        query = f"SELECT * FROM {table_name} LIMIT 1;"
        return self.execute_query(query)[0]

    def delete_count(self, table_name: str, limit: int) -> None:
        query = f"DELETE FROM {table_name} LIMIT {limit};"
        return self.execute_query(query)

    def delete_first_row(self, table_name: str) -> None:
        query = f"DELETE FROM {table_name} LIMIT 1;"
        return self.execute_query(query)


# if __name__ == '__main__':
#     host = const.HOST
#     user = const.USER
#     password = const.PASSWORD
#     database_name = const.DATABASE_NAME
#     db_obj = database(
#         host = host,
#         user = user,
#         password=password,
#         database = database_name,
#     )
#     db_obj.connect()
#     db_obj.execute_query('show databases')
#     db_obj.insert(const.TABLE_NAME , ['links'],['hello1'])
#     # db_obj.eraze_table(const.TABLE_NAME)
#     data = db_obj.swap_table(const.TABLE_NAME)
#     print(type(data))
#     print(data[0][0])
#     db_obj.commit_changes()
#     db_obj.disconnect()
