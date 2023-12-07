import pymysql
from controller.category import Category
from controller.condition import Condition
from controller.grant import Grant
from controller.location import Location
from controller.owner import Owner
from controller.equipment import Equipment
class Database(Category,Condition,Grant,Location,Owner,Equipment):
    def __init__(self):
        pass
    def connect(self):
        # return pymysql.connect("mysql", "dev", "dev", "crud_flask")

        return pymysql.connect(host="mysql", user="dev", password="dev", database="crud_flask", charset='utf8')