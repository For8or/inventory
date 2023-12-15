import pymysql
import logging

class User():
    def __init__(self):
        pass
    def read_user(self,name):
        con = pymysql.connect(host="mysql", user="dev", password="dev", database="crud_flask", charset='utf8')
        cursor = con.cursor()

        try:
            if name == None:
                cursor.execute("SELECT * FROM user_table order by name asc")
            else:
                cursor.execute(
                    "SELECT * FROM user_table where name = %s order by name asc", (name,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()
            
    def read_user_id(self,id):
        con = pymysql.connect(host="mysql", user="dev", password="dev", database="crud_flask", charset='utf8')
        cursor = con.cursor()

        try:
            if id:
                cursor.execute(
                    "SELECT * FROM user_table where id = %s order by name asc", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()             
    def insert_user(self, data):
        con = pymysql.connect(host="mysql", user="dev", password="dev", database="crud_flask", charset='utf8')
        cursor = con.cursor()
        logging.info("Inserting user data: %s", data)


        try:
            # Correct the SQL INSERT statement
            cursor.execute("INSERT INTO user_table (name, password_hash, role, is_first_login) VALUES (%s, %s, %s, %s)",
                        (data['username'], data['password_hash'], data['role'], data['is_first_login']))
            con.commit()
            return True
        except Exception as e:
            logging.error("Database Insert Error: %s", e)
            con.rollback()
            return False
        finally:
            con.close()


    def update_user_password(self, id, data):
        con =  pymysql.connect(host="mysql", user="dev", password="dev", database="crud_flask", charset='utf8')
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE user_table set password_hash = %s where id = %s",
                           (data, id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def update_user_first_login(self, id, data):
        con =  pymysql.connect(host="mysql", user="dev", password="dev", database="crud_flask", charset='utf8')
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE user_table set is_first_login = %s where id = %s",
                           (data, id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()
    def delete_user(self, id):
        con =  pymysql.connect(host="mysql", user="dev", password="dev", database="crud_flask", charset='utf8')
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM user_table where id = %s", (id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()