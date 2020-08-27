from app import *
from datetime import datetime
from datetime import date
import schedule
import time
def main():
    new_ids = check_for_new()
    if not new_ids:
        print('Updated ' + str(datetime.now()))
        print("No new mails")
        return 1
    spam = spamcheck(new_ids)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="########",
        )
    cursor = mydb.cursor()
    cursor.execute('use emails')
    f = open('/Users/gautamvenkatesh/Coding/testgmail/log.txt', 'a')
    f.write('\nAccessed on ' + str(datetime.now()))
    f.close()
    print('Updated ' + str(datetime.now()))
    for i in spam:
        if spam[i]:
            cont = getinformation(i)
            print('spam')
            cursor.execute('insert into spamhtml (html, subject, date, readed, name, emailadd) values (%s,%s,%s,%s,%s,%s)', (gethtml(i), cont['subject'], cont['date'], False, cont['name'], cont['emailadd']))
        elif not spam[i]:
            print('worked')
            cont = getinformation(i)
            cursor.execute('insert into html (cont, subject, date, readed, name, emailadd) values (%s,%s,%s,%s,%s,%s)', (gethtml(i), cont['subject'], cont['date'], False, cont['name'], cont['emailadd']))
    mydb.commit()
    cursor.close()
    updatedb()


def spam():
    print('spam email sent')
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="########!",
        )
    cursor = mydb.cursor()
    cursor.execute('use emails')
    cursor.execute('select * from spamhtml')
    emails = cursor.fetchmany(100)
    html = ""
    for i in emails:
        html += (i[0])
        html += "<p>\n\n--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n</p>"
    cursor.execute("insert into html (cont, subject, date, readed, name, emailadd) values (%s,%s,%s,%s,%s,%s)", (html, "Spam", date.today(), False, 'Gautam', 'vegautam@gmail.com'))
    cursor.execute("delete from spamhtml")
    mydb.commit()
    cursor.close()


schedule.every().day.at('17:00').do(spam)
schedule.every(15).minutes.do(main)
main()
while True:
    try:
        schedule.run_pending()
    except TimeoutError as te:
        print("timeout error occurred")
    except KeyboardInterrupt:
        pass;
    except Exception as e:
        print("unkown error occurred")
        print(e)

    time.sleep(450)
