import sqlite3


class Authorization_Table_Lite:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)

    def get_users(self, machine_id):
        conn = self.conn
        result = dict()
        i = 0
        query = "SELECT * from Authorization WHERE machine_id = ?"
        for row in conn.execute(query, [machine_id]):
            result[i] = dict()
            result[i]['user_id'] = row[0]
            result[i]['machine_id'] = row[1]
            i += 1
        return result

    def get_machines(self, user_id):
        conn = self.conn
        result = dict()
        i = 0
        query = "SELECT * from Authorization WHERE user_id = ?"
        for row in conn.execute(query, [user_id]):
            result[i] = dict()
            result[i]['user_id'] = row[0]
            result[i]['machine_id'] = row[1]
            i += 1
        return result

    def authorize(self,user_id, machine_id):
        conn = self.conn
        c = conn.cursor()
        query = "INSERT INTO Authorization VALUES(?,?)"
        try:
            c.execute(query, [user_id, machine_id])
        except sqlite3.IntegrityError:
            print("authorization already exists")
            return 1  # Fail code
        except:
            print("error executing the query")
            return 2
        conn.commit()
        return 0
