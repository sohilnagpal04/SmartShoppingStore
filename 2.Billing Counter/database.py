import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="pi",
  database="mydatabase"
)

mycursor = mydb.cursor()
#sql = "DELETE FROM shop WHERE name = 'samarth'"
#mycursor.execute(sql)
#mydb.commit()
print("All Account")
print("============")
sql = "SELECT * FROM shop"
mycursor.execute(sql)
myresult = mycursor.fetchall()

for x in myresult:
    print(x)
