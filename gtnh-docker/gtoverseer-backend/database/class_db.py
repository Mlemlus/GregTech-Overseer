import psycopg2, sys

class db: # Database class, opens the connection and executes cursor commands with its functions, on destruction closes database connection
    def __init__(self, connection_parameters):
        self.conn = None # Connection variable
        # Opening the database connection
        try:
            self.conn = psycopg2.connect(**connection_parameters) # connect to postgres with parameters, ** unpacks dict
        except Exception as e:
            print(f"db: failed to connect to the database: {e}", file=sys.stderr)

    def __del__(self): # class destruction function
        if self.conn:
            self.conn.close() # close the db connection
            self.conn = None

    def insert(self, query, values):
        cur = self.conn.cursor() # Opens a new cursor
        try:
            cur.execute(query, values) 
            self.conn.commit()
            return True, None
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
            return True, vals
        except Exception as e:
            self.conn.rollback()
            return False, e
        finally:
            cur.close()

    def selectSingle(self, query, value):
        cur = self.conn.cursor()
        try:
            cur.execute(query, (value,))
            val = cur.fetchone()
            return True, val
        except Exception as e:
            self.conn.rollback()
            return False, e
        finally:
            cur.close()

    def selectMultiple(self, query, value):
        cur = self.conn.cursor()
        try:
            cur.execute(query, value)
            val = cur.fetchone()
            return True, val
        except Exception as e:
            self.conn.rollback()
            return False, e
        finally:
            cur.close()

    def selectReturnMultiple(self, query, values):
        cur = self.conn.cursor()
        try:
            cur.execute(query, values)
            vals = cur.fetchall()
            return True, vals
        except Exception as e:
            self.conn.rollback()
            return False, e
        finally:
            cur.close()

    def update(self, query, values):
        cur = self.conn.cursor()
        try:
            cur.execute(query, values)
            self.conn.commit()
            return True, None
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
            return True, None
        except Exception as e:
            self.conn.rollback()
            return False, e
        finally:
            cur.close()
