#! /usr/bin/env python
import psycopg2

DATABASE_NAME = "news"


# Database query function
def query_db(query):
    ''' Makes a query to the news database '''
    db = psycopg2.connect(database=DATABASE_NAME)
    c = db.cursor()
    c.execute(query)
    return c.fetchall()
    db.close()


# 1. What are the most popular three articles of all time?
# Which articles have been accessed the most?
# Present this information as a sorted list with
# the most popular article at the top.

def three_most_popular_articles():
    # To print information
    information_string = '1. The 3 most popular articles of all time are:\n'

    # Query string
    query = "select title,count(*) as num from " \
            "articles,log where " \
            "log.path=CONCAT('/article/',articles.slug) " \
            "group by articles.title " \
            "order by num DESC limit 3;"

    print(information_string)
    for result in query_db(query):
        print('\t"' + str(result[0]) + '" - ' + str(result[1]) + ' views')

    print("\n")


# 2. Who are the most popular article authors of all time?
#  That is, when you sum up all of the articles each author
#  has written, which authors get the most page views?
#  Present this as a sorted list with the most popular
#  author at the top.
def most_popular_article_authors():
    # To print information
    information_string = '2. The most popular article ' \
                         'authors of all time are:\n'

    # Query string
    query = " select x.author , count(1) as qtd from (" \
            " SELECT b.name as author" \
            " FROM articles a join authors b on(a.author = b.id)" \
            " join log c on(c.path = '/article/' ||a.slug)" \
            " ) x group by x.author order by 2 desc limit 3;"

    print(information_string)
    for result in query_db(query):
        print('\t' + str(result[0]) + ' - ' + str(result[1]) + ' views')

    print("\n")


# 3. On which days did more than 1% of requests
#  lead to errors? The log table includes a column
#  status that indicates the HTTP status code that
#  the news site sent to the user's browser.
# (Refer back to this lesson if you want to
#  review the idea of HTTP status codes.)
def days_with_request():
    # To print information
    information_string = '3. Days with more than ' \
                         '1% of request that lead to an error:\n'

    # Query string
    query = "select * from (select date(time)," \
            "round(100.0*sum(case log.status " \
            "when '200 OK'  then 0 else 1 end)/count(log.status),3)" \
            " as error from log group by date(time) " \
            "order by error desc) as subq where error > 1;"

    print(information_string)
    for result in query_db(query):
        date = str((result[0]).strftime("%B %d, %Y"))
        print('\t' + date + ' - ' + str(result[1]) + ' %')

    print("\n")


# printing out results below
three_most_popular_articles()
most_popular_article_authors()
days_with_request()
