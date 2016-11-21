import sqlite3

class Machine_Table_Lite:
    def __init__(self, database_name='blobs.db'):
        self.conn = sqlite3.connect(database_name)

    def get_name(self, id):
        conn = self.conn
        c = conn.cursor()
        query = "SELECT * from Machine WHERE id = ?"
        c.execute(query, [id])
        row = c.fetchone()
        result = dict()
        result[0] = dict()
        result[0]['id'] = row[0]
        result[0]['name'] = row[1]
        return result


    def set_machine(self, id, name):
        conn = self.conn
        c = conn.cursor()
        query = "INSERT INTO Machine VALUES(?,?)"
        try:
            c.execute(query, [id, name])
        except sqlite3.IntegrityError:
            print("duplicate data")
            return 1 #Fail code
        except:
            print("error executing the query")
            return 2
        conn.commit()
        return 0

    def set_conn(self,conn):
        self.conn = conn