import logging
import pymysql

class Equipment():
    def __init__(self):
        pass
    def read_equipment(self,id):
        con = pymysql.connect(host="mysql", user="dev", password="dev", database="crud_flask", charset='utf8')
        cursor = con.cursor()
        try:
            if id == None:
                cursor.execute("SELECT * FROM equipment_table order by wia asc")
                return cursor.fetchall(), "none"
            else:
                cursor.execute(
                    "SELECT * FROM equipment_table where id = %s order by wia asc", (id,))
                data = cursor.fetchall()
                logging.warning(data[0][1]) 
                cursor.execute(
                    "SELECT * FROM funding_table where equipment_id = %s", (data[0][1],))
                funding = cursor.fetchall()
                return data,funding
            
        except Exception as e:
            logging.error(f"Error: {e}")
            return ()
        finally:
            con.close()
                  
    def insert_equipment(self,wia,category,cost,aquired,description_field,serial_field,owner_field,use_field,location_field,condition_field,inspection,disposition,grant_data,notes):
        con =  pymysql.connect(host="mysql", user="dev", password="dev", database="crud_flask", charset='utf8')
        cursor = con.cursor()
        try:
            cursor.execute("INSERT INTO equipment_table(wia,category,cost,aquired,description_field,serial_field,owner_field,use_field,location_field,condition_field,inspection,disposition,notes) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (wia,category,cost,aquired,description_field,serial_field,owner_field,use_field,location_field,condition_field,inspection,disposition,notes))
            con.commit()
            for i in range(0, len(grant_data),2):
                    cursor.execute("INSERT INTO funding_table (name, percentage, equipment_id) VALUES (%s, %s, %s)", (grant_data[i], grant_data[i+1], wia))
                    con.commit()
            return True
        except Exception as e:
            logging.error(f"Error: {e}")
            con.rollback()

            return False
        finally:
            con.close()

    def update_equipment(self, wia, category, cost, aquired, description_field, serial_field, owner_field, use_field, location_field, condition_field, inspection, disposition, grant_data, notes, id):
        con = pymysql.connect(host="mysql", user="dev", password="dev", database="crud_flask", charset='utf8')
        cursor = con.cursor()
        try:
            # Update the equipment_table
            cursor.execute("UPDATE equipment_table set wia = %s, category = %s, cost = %s, aquired = %s, description_field = %s, serial_field = %s, owner_field = %s, use_field = %s, location_field = %s, condition_field = %s, inspection = %s, disposition = %s, notes = %s where id = %s",
                           (wia, category, cost, aquired, description_field, serial_field, owner_field, use_field, location_field, condition_field, inspection, disposition, notes, id))
            con.commit()

            # Update the funding_table
            # First, clear existing funding entries for this equipment
            cursor.execute("DELETE FROM funding_table WHERE equipment_id = %s", (wia,))
            con.commit()

            # Then, insert new/updated funding entries
            for i in range(0, len(grant_data), 2):
                cursor.execute("INSERT INTO funding_table (name, percentage, equipment_id) VALUES (%s, %s, %s)", (grant_data[i], grant_data[i+1], wia))
                con.commit()

            return True
        except Exception as e:
            logging.error(f"Error in update_equipment: {e}")
            con.rollback()
            return False
        finally:
            con.close()

    def delete_equipment(self, id):
        con =  pymysql.connect(host="mysql", user="dev", password="dev", database="crud_flask", charset='utf8')
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM equipment_table where id = %s", (id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()