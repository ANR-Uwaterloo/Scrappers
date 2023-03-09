import mysql.connector
import config.config as cfg

#
# class Database_Wrapper extends mysql.connector:
#
#     conf = {}
#     db = object
#     def __init__(self):
#         self.conf = cfg.read_config()
#
#     def db_connect(self):
#         # Connect to server
#         self.db = mysql.connector.connect(
#             host = self.conf["host"],
#             port = self.conf["port"],
#             user = self.conf["user"],
#             password = self.conf["password"],
#             db = self.conf["db"]
#         )
#         print(self.db)
#         return self.db
#
#     def db_get_cursor(self):
#         return self.db.cursor()
#
#     def db_commit(self, statement):
#         self.db.execute(statement)
#         self.db.commit()
#
#     def db_close_connection(self):
#         self.db.close()

def db_connection(conf):
    db_cn = mysql.connector.connect(
                host = conf["host"],
                port = conf["port"],
                user = conf["user"],
                password = conf["password"],
                db = conf["db"]
            )
    return db_cn

