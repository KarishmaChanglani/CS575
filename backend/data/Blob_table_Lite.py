import sqlite3

class Blob_Table_Lite:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)

    "Returns 1 fail code if duplicate, 2 if error ezecuting and 0 on success"
    def add_record(self, machine_id, datetime, categoy, blob):
        query = "INSERT INTO Blobs VALUES(?,?,?,?)"
        conn = self.conn
        c = conn.cursor()
        try:
            c.execute(query, [machine_id, datetime, categoy, blob])
        except sqlite3.IntegrityError:
            print("duplicate data")
            return 1 #Fail code
        except:
            print("error executing the query")
            return 2
        conn.commit()
        return 0

    def get_records(self, start, count, machine_id, category):
        conn = self.conn
        query = 'SELECT * from Blobs WHERE Machine_id = ? AND category_name = ? ;'
        result = dict()
        i = 0
        for row in conn.execute(query, [machine_id, category]):
            if i < start + count - 1 and i >= start - 1:
                result[i] = dict()
                result[i]['machine_id'] = row[0]
                result[i]['datetime'] = row[1]
                result[i]['category'] = row[2]
                result[i]['data'] = row[3]
            i += 1

        return result

    """to close the connection object before destroying the object"""
    def close_connection(self):
        self.conn.close()