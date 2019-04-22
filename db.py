from mysql.connector import connect

def connectDB(host='localhost',database='hosteldb',user='dbmspro',password='password',):
    return connect(host=host,database=database,user=user,password=password)
