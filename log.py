# !/usr/bin/env python3
# Log Project
# Database used (news)


import psycopg2

dbname = "news"
try:
    db = psycopg2.connect(database=dbname)
except:
    print ("Unable to connect to the database")


def get_top_post():
    db = psycopg2.connect(database=dbname)
    c = db.cursor()
    c.execute('''SELECT toparticles.title, CONCAT(toparticles.count, ' views')
                FROM toparticles
                LIMIT 3''')

    for i in c.fetchall():
        print(str(i[0]) + '---' + str(i[1]))
    db.close()


print('The top three articles are:')
get_top_post()


def get_top_authors():
    db = psycopg2.connect(database=dbname)
    c = db.cursor()
    c.execute('''SELECT auth.name, SUM(toparticles.count) as total
                FROM toparticles join auth
                ON toparticles.title = auth.title
                GROUP BY auth.name
                ORDER BY total desc
                LIMIT 3''')

    for i in c.fetchall():
        print(str(i[0]) + '---' + str(i[1]) + ' views')
    db.close()


print('\nThe top three authors are:')
get_top_authors()


def get_errors():
    db = psycopg2.connect(database=dbname)
    c = db.cursor()
    c.execute('''SELECT date, percentage
                FROM logerrors
                WHERE percentage > 1''')

    for i in c.fetchall():
        print(i[0], str(i[1])+'%')
    db.close()


print('\nDays with more than 1% are:')
get_errors()
