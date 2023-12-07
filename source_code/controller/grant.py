import pymysql

class Grant():
    def __init__(self):
        pass
    def read_grant(self,id):
        con = pymysql.connect(host="mysql", user="dev", password="dev", database="crud_flask", charset='utf8')
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM grant_table order by name asc")
            else:
                cursor.execute(
                    "SELECT * FROM grant_table where id = %s order by name asc", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()
                  
    def insert_grant(self, data):
        con =  pymysql.connect(host="mysql", user="dev", password="dev", database="crud_flask", charset='utf8')
        cursor = con.cursor()

        try:
            cursor.execute("INSERT INTO grant_table(name,fain,federal) VALUES(%s,%s,%s)",
                           (data['name'],data['fain'],data['federal']))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def update_grant(self, id, data):
        con =  pymysql.connect(host="mysql", user="dev", password="dev", database="crud_flask", charset='utf8')
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE grant_table set name = %s, fain = %s, federal = %s where id = %s",
                           (data['name'],data['fain'],data['federal'], id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def delete_grant(self, id):
        con =  pymysql.connect(host="mysql", user="dev", password="dev", database="crud_flask", charset='utf8')
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM grant_table where id = %s", (id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()