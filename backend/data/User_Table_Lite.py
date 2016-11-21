import sqlite3

class User_Table_Lite:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)


    """returns records that start at rowid start-1 and gives count no""" \
    """of rows or less. It returns in the form of a dictionary"""
    def get_records(self, start, count):
        conn = self.conn
        query = 'SELECT * from User;'
        result = dict()
        i = 0
        for row in conn.execute(query):
            if i < start+count-1 and i >= start-1 :
                result[i] = dict()
                result[i]['id'] = row[0]
                result[i]['token'] = row[1]
            i += 1

        return result


    """returns the User with the given id in the form if a dictionary"""
    def get_User(self,id):
        conn = self.conn
        query = "SElECT * from User WHERE id = ?;"
        c = conn.cursor()
        c.execute(query, [id])
        row = c.fetchone()
        result = dict()
        result[0] = dict()
        result[0]['id'] = row[0]
        result[0]['token'] = row[1]
        return result


    """Addes user with id and token to the User table, returns error code 1
    if the user already exists and 2 for any other error"""
    def set_User(self, id, token):
        conn = self.conn
        query = "INSERT INTO User VALUES(?, ?)"
        c = conn.cursor()
        try:
            c.execute(query, [id, token])
        except sqlite3.IntegrityError:
            print("couldn't add the user twice")
            return 1 #Fail code
        except:
            print("error executing the query")
            return 2
        conn.commit()
        return 0


    """to close the connection object before destroying the object"""
    def close_connection(self):
        self.conn.close()