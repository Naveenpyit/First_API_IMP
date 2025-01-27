from .mainconnection import connection

class api_methods():
    @staticmethod
    def get(query):
       try:
            conn=connection.db_connection()
            cursor=conn.cursor()
            cursor.execute(query)
            col_name=[desc[0] for desc in cursor.description]
            rows=cursor.fetchall()
            conn.close()
            cursor.close()
            res=[dict(zip(col_name,row))for row in rows]
            return res
       except Exception as e:
           return {"Error":str(e)}
       
    @staticmethod
    def post(query,params):
        try:
            conn=connection.db_connection()
            cur=conn.cursor()
            cur.execute(query,params)
            conn.commit()
            conn.close()
            cur.close()
            return {"Message":"Data Submitted Successfully"}
        except Exception as err:
            return {"Error":str(err)}
        
    @staticmethod
    def put(query,params):
        try:
            conn=connection.db_connection()
            cur=conn.cursor()
            cur.execute(query,params)
            conn.commit()
            conn.close()
            cur.close()
            return {"Message":"Updated Successfully"}
        except Exception as err:
            return {"Error":str(err)}
        
    @staticmethod
    def delete(query,para):
        try:
            conn=connection.db_connection()
            cur=conn.cursor()
            cur.execute(query,para)
            conn.commit()
            conn.close()
            cur.close()
            return {"Message":"Deleted Succesfully!"} 
        except Exception as err:
            return {"Error":str(err)}   

