import pymysql

class Owner():
    def __init__(self):
        pass
    def read_owner(self,id):
        con = pymysql.connect(host="mysql", user="dev", password="dev", database="crud_flask", charset='utf8')
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM owner_table order by name asc")
            else:
                cursor.execute(
                    "SELECT * FROM owner_table where id = %s order by name asc", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()
                  
    def insert_owner(self, data):
        con =  pymysql.connect(host="mysql", user="dev", password="dev", database="crud_flask", charset='utf8')
        cursor = con.cursor()

        try:
            cursor.execute("INSERT INTO owner_table(name) VALUES(%s)",
                           (data['name'],))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def update_owner(self, id, data):
        con =  pymysql.connect(host="mysql", user="dev", password="dev", database="crud_flask", charset='utf8')
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE owner_table set name = %s where id = %s",
                           (data['name'], id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def delete_owner(self, id):
        con =  pymysql.connect(host="mysql", user="dev", password="dev", database="crud_flask", charset='utf8')
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM owner_table where id = %s", (id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()