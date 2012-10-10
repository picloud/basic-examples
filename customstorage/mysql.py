"""
Queries your MySQL Database from your local machine, and from PiCloud.
You need to fill in your MySQL hostname, db, and credentials.
"""

HOST = ''
USER = ''
PASSWD = ''
DBNAME = ''

import MySQLdb

def list_of_all_tables():
    conn = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DBNAME)
    cursor = conn.cursor()
    cursor.execute('show tables')
    return cursor.fetchall()

print 'Running locally', list_of_all_tables()

jid = cloud.call(list_of_all_tables)
print 'Running on the cloud', cloud.result(jid)

