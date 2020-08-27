# spamemails

This is the code I used to make a website that shows my emails, filters out spam emails, and sends a daily email with all the spam received in the previous 24 hours.
This code is not meant for public use, and is merely to showcase my work.

The code uses the django framework. A seperate script (main.py and app.py) checks emails, classifies them, and updates a database with new emails, including the daily spam email. The website gets emails from the database and displays them.
The spam filter used will be updated to use a machine learning classification soon.
