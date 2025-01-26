from decouple import config # type: ignore
import psycopg2 # type: ignore


def db_connection():
    return psycopg2.connect(
        dbname=config('DB_NAME'),
        user=config('DB_USER'),
        password=config('DB_PASSWORD'),
        host=config('DB_HOST'),
        port=config('DB_PORT')
    )

class api_gets():
    @staticmethod
    def ph_prod_cata(query):
       try:
            conn=db_connection()
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
    def ph_bussiness(query):
        try:
            conn=db_connection()
            cur=conn.cursor()
            cur.execute(query)
            column=[d[0]for d in cur.description]
            rows=cur.fetchall()
            conn.close()
            cur.close()
            result=[dict(zip(column,row))for row in rows]
            return result
        except Exception as e:
            return {"Error":str(e)}   

#postmethods
class api_post():
    @staticmethod
    def post_ph_bussiness(query,params):
        try:
            conn=db_connection()
            cur=conn.cursor()
            cur.execute(query,params)
            conn.commit()
            conn.close()
            cur.close()
            return {"Success":"Data Submitted Successfully"}
        except Exception as err:
            return {"Error":str(err)}


class api_put():
    @staticmethod
    def put_ph_business(query,params):
        try:
            conn=db_connection()
            cur=conn.cursor()
            cur.execute(query,params)
            conn.commit()
            conn.close()
            cur.close()
            return {"Message":"Updated Successfully"}
        except Exception as err:
            return {"Error":str(err)}