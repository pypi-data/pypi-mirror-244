import pymysql
from urllib.parse import urlparse
from .types.log_entry import LogEntry

class SQLAdapter:
    @staticmethod
    def connect_to_database(db_url):
        parsed_url = urlparse(db_url)
        username = parsed_url.username
        password = parsed_url.password
        host = parsed_url.hostname
        port = parsed_url.port
        database = parsed_url.path.lstrip('/')

        # Establishing a connection to the MySQL database
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection

    @staticmethod
    def execute_query(connection, table, query, limit):
        result_array = []
        try:
            with connection.cursor() as cursor:
                sql = query
                cursor.execute(sql % (table,limit))
                result_array = cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            connection.close()

        return result_array

    def fetch_log_entries(self, db_url, table, query, limit):
        try:
            db_connection = self.connect_to_database(db_url)
            log_entries = self.execute_query(db_connection, table, query, limit)
            adapted_log_antries = [LogEntry(**log_entry) for log_entry in log_entries]
            return adapted_log_antries
        except Exception as e:
            raise e
