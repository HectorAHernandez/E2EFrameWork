# "Reading Records From the Database
# Until now, you’ve been building your database. Now it’s time to perform some queries on it and find some interesting
# properties from this dataset. In this section, you’ll learn how to read records from database tables using
# the SELECT statement.
#
# Reading Records Using the SELECT Statement
# To retrieve records, you need to send a SELECT query to cursor.execute(). Then you use cursor.fetchall() to
# extract the retrieved table in the form of a list of rows or records.
#
# Try writing a MySQL query to select all records from the movies table and send it to"
from mysql.connector import connect, Error

try:
    with connect(
        host="localhost",
        user="hector",
        password="saibaba0",
        database="online_movie_rating"
    ) as db_connection:
        select_movies_query = "SELECT * FROM movies limit 5"
        with db_connection.cursor() as cursor:
            cursor.execute(select_movies_query)
            result = cursor.fetchall()
except Error as err:
    print("database connection error: ", err)

for row in result:
    print("Whole result in row: ", row)
    id = row[0]
    title = row[1]
    year = row[2]
    genere = row[3]
    money_collected = row[4]
    print("id: {} title {}, year: {}, genere {} money made {}".format(id, title, year, genere, money_collected))

# "The result variable holds the records returned from using .fetchall(). It’s a list of tuples representing individual
# records from the table.
#
# In the query above, you use the LIMIT clause to constrain the number of rows that are received from the SELECT
# statement. Developers often use LIMIT to perform pagination when handling large volumes of data.
#
# In MySQL, the LIMIT clause takes one or two nonnegative numeric arguments. When using one argument, you specify the
# maximum number of rows to return. Since your query includes LIMIT 5, only the first 5 records are fetched. When
# using both arguments, you can also specify the offset of the first row to return:
#
# SELECT * FROM movies LIMIT 2,5;
# The first argument specifies an offset of 2, and the second argument constrains the number of returned rows to 5.
# The above query will return rows 3 to 7.
# You can also query for selected columns:"
try:
    with connect(
        host="localhost",
        user="hector",
        password="saibaba0",
        database="online_movie_rating"
    ) as db_connection:
        select_movies_query = "SELECT title, release_year FROM movies LIMIT 2,5"
        with db_connection.cursor() as cursor:
            cursor.execute(select_movies_query)
            for row in cursor.fetchall():
                print("row: ", row)
except Error as err:
    print("database connection error: ", err)

# "MySQL offers a plethora of string formatting operations like CONCAT for concatenating strings. Often, websites will
# show the movie title along with its release year to avoid confusion. To retrieve the titles of the top five grossing
# movies, concatenated with their release years, you can write the following query:
#
try:
    with connect(
        host="localhost",
        user="hector",
        password="saibaba0",
        database="online_movie_rating"
    ) as db_connection:
        select_movies_query = """
         SELECT CONCAT(title, " (", release_year, ")"),
               collection_in_mil
         FROM movies
         ORDER BY collection_in_mil DESC
         LIMIT 5
         """
        with db_connection.cursor() as cursor:
            cursor.execute(select_movies_query)
            for movie in cursor.fetchall():
                print("movie: ", movie)
except Error as err:
    print("database connection error: ", err)

# If you don’t want to use the LIMIT clause and you don’t need to fetch all the records, then the cursor object
# has .fetchone() and .fetchmany() methods as well:
#
# .fetchone() retrieves either the next row of the result, as a tuple, or None if no more rows are available.
# .fetchmany() retrieves the next set of rows from the result as a list of tuples. It has a size argument, which
# defaults to 1, that you can use to specify the number of rows you need to fetch. If no more rows are available, then
# the method returns an empty list.
# Try retrieving the titles of the five highest-grossing movies concatenated with their release years again, but this
# time use .fetchmany():"