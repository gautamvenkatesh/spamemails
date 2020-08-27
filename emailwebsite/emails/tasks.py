import mysql.connector

def get_reg_html():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="#######",
        )
    cursor = mydb.cursor( buffered = True)
    cursor.execute('use emails')
    cursor.execute("select * from html order by ID desc")
    htmlraw = cursor.fetchmany(30)
    cursor.close()
    return htmlraw



def deleter(ids):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="#######",
        )
    cursor = mydb.cursor( buffered = True)
    cursor.execute('use emails')
    cursor.execute(f"delete from html where ID = {ids}")
    mydb.commit()
    return 0
