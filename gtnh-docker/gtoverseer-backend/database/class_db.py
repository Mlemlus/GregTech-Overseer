import psycopg2, sys

class db:
    def __init__(self, connection_parameters):
        self.conn = None
        # Opening the database connection
        try:
            self.conn = psycopg2.connect(**connection_parameters) # connect to postgres with parameters
        except Exception as e:
            print(f"failed to connect to the database: {e}", file=sys.stderr)

    def __del__(self): # class destruction function
        if self.conn:
            self.conn.close() # close the db connection
            self.conn = None

    def insert(self, query, values):
        cur = self.conn.cursor() # Opens a new cursor
        try:
            cur.execute(query, values) # Executes the query with the values
            self.conn.commit()
            cur.close()
        except Exception as e:
            self.conn.rollback() # rollback when error
            return False, e
        finally:
            cur.close()
    
    def select(self, query):
        cur = self.conn.cursor()
        try:
            cur.execute(query)
            vals = cur.fetchall()
            return vals
        except Exception as e:
            self.conn.rollback() # idk if necessary 
            return False, e
        finally:
            cur.close()

    def selectSingle(self, query, value):
        cur = self.conn.cursor()
        try:
            cur.execute(query, (value,))
            val = cur.fetchone()
            return val
        except Exception as e:
            self.conn.rollback() # idk if necessary 
            return False, e
        finally:
            cur.close()
    
    def update(self, query, values):
        cur = self.conn.cursor()
        try:
            cur.execute(query, values)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            return False, e
        finally:
            cur.close()
    
    def delete(self, query, values):
        cur = self.conn.cursor()
        try:
            cur.execute(query, values)
            self.conn.commit()
            return True 
        except Exception as e:
            return False, e
        finally:
            cur.close()
