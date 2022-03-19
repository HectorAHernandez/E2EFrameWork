#   ****** This database example included in the serie of code testhh_06_xx can be found at this website
#   https://realpython.com/python-mysql/

# "Connecting to an Existing Database
# In the last section, you created a new database called online_movie_rating. However, you still haven’t
# connected to it. In many situations, you’ll already have a MySQL database that you want to connect with your
# Python application.
#
# You can do this using the same connect() function that you used earlier by sending an additional parameter
# called database:

from mysql.connector import connect, Error

# to list all the databases defined in the server:
try:
    with connect(
        host="localhost",
        # user=input("Enter user name:"),
        user="hector",
        # password=getpass("Enter password: ")
        password="saibaba0",
    ) as db_connection:
        print("database connection: ", db_connection)
        show_database_query = "SHOW DATABASES"
        with db_connection.cursor() as cursor:
            cursor.execute(show_database_query)
            for db in cursor:
                print("Database name: ", db)
except Error as err:
    print("The DB Connection or Query error is: ", err)

# "Creating, Altering, and Dropping a Table
# In this section, you’ll learn how to perform some basic DDL queries like CREATE, DROP, and ALTER with Python. You’ll
# get a quick look at the MySQL database that you’ll use in the rest of this tutorial. You’ll also create all the
# tables required for the database and learn how to perform modifications on these tables later on.
#
# Defining the Database Schema
# You can start by creating a database schema for an online movie rating system. The database will consist of
# three tables: movie, reviewers and ratings"

# Creating movies table:
try:
    with connect(
        host="localhost",
        user="hector",
        password="saibaba0",
        database="online_movie_rating"
    ) as db_connection:
        create_table_query = """
            CREATE TABLE ratings (
                movie_id INT,
                reviewer_id INT,
                rating DECIMAL(2,1),
                FOREIGN KEY(movie_id) REFERENCES movies(id),
                FOREIGN KEY(reviewer_id) REFERENCES reviewers(id),
                PRIMARY KEY(movie_id, reviewer_id)
            )
            """
        with db_connection.cursor() as cursor:
            cursor.execute(create_table_query)
            db_connection.commit()
            print("*** changes committed")
except Error as err:
    print("The DB Connection or Query error is: ", err)

# "Also, notice the connection.commit() statement at the end of the code. By default, your MySQL connector doesn’t
# autocommit transactions. In MySQL, modifications mentioned in a transaction occur only when you use a COMMIT
# command in the end. Always call this method after every transaction to perform changes in the actual table."

# "The implementation of foreign key relationships in MySQL is slightly different and limited as compared to the
# standard SQL. In MySQL, both the parent and the child in the foreign key constraint must use the same storage engine.

# A storage engine is the underlying software component that a database management system uses for performing SQL
# operations. In MySQL, storage engines come in two different flavors:
#
# Transactional storage engines are transaction safe and allow you to roll back transactions using simple commands
# like rollback. Many popular MySQL engines, including InnoDB and NDB, belong to this category.
#
# Nontransactional storage engines depend on elaborate manual code to undo statements committed on a database. MyISAM,
# MEMORY, and many other MySQL engines are nontransactional.
#
# InnoDB is the default and most popular storage engine. It helps maintain data integrity by supporting foreign key
# constraints. This means that any CRUD operation on a foreign key is checked to ensure that it doesn’t lead to
# inconsistencies across different tables.
#
# Also, note that the ratings table uses the columns movie_id and reviewer_id, both foreign keys, jointly as the
# primary key. This step ensures that a reviewer can’t rate the same movie twice.
#
# You may choose to reuse the same cursor for multiple executions. In that case, all executions would become one
# atomic transaction rather than multiple separate transactions. For example, you can execute all CREATE TABLE
# statements with one cursor and then commit your transaction only once:

# try:
#     with connect(
#         host="localhost",
#         user="hector",
#         password="saibaba0",
#         database="online_movie_rating"
#     ) as db_connection_02:
#         with db_connection_02.cursor() as cursor:
#             cursor.execute(create_movies_table_query)
#             cursor.execute(create_reviewers_table_query)
#             cursor.execute(create_ratings_table_query)
#             db_connection_02.commit()
# except Error as err:
#     print("database connection error: ", err)

# The above code will first execute all three CREATE statements. Then it will send a COMMIT command to the MySQL
# server that commits your transaction. You can also use .rollback() to send a ROLLBACK command to the MySQL server
# and remove all data changes from the transaction.

# "Showing a Table Schema Using the DESCRIBE Statement
# Now, that you’ve created all three tables, you can look at their schema using the following SQL statement:
# DESCRIBE <table_name>;
# To get some results back from the cursor object, you need to use cursor.fetchall(). This method fetches all rows
# from the last executed statement. Assuming you already have the MySQLConnection object in the connection variable,
# you can print out all the results fetched by cursor.fetchall():
try:
    with connect(
        host="localhost",
        user="hector",
        password="saibaba0",
        database="online_movie_rating"
    ) as db_connection:
        db_query = "DESCRIBE movies"
        with db_connection.cursor() as cursor:
            cursor.execute(db_query)
            # Fetch all rows from the just executed query
            result = cursor.fetchall()
            for row in result:
                print("row = ", row)
except Error as err:
    print("database connection error: ", err)

# "Modifying a Table Schema Using the ALTER Statement
# In the movies table, you have a column called collection_in_mil, which contains a movie’s box office collection in
# millions of dollars. You can write the following MySQL statement to modify the data type of collection_in_mil
# attribute from INT to DECIMAL:
# ALTER TABLE movies MODIFY COLUMN collection_in_mil DECIMAL(4,1);
# DECIMAL(4,1) means a decimal number that can have a maximum of 4 digits, of which 1 is decimal, such as 120.1, 3.4,
# 38.0, and so on. After executing the ALTER TABLE statement, you can show the updated table schema using DESCRIBE:"
try:
    with connect(
        host="localhost",
        user="hector",
        password="saibaba0",
        database="online_movie_rating"
    ) as db_connection:
        alter_table_query = """
            ALTER TABLE movies 
            MODIFY COLUMN collection_in_mil DECIMAL(4,1)
            """
        show_table_query = "DESCRIBE movies"
        with db_connection.cursor() as cursor:
            cursor.execute(alter_table_query)
            cursor.execute(show_table_query)
            # fetch all rows from lastes executed query
            result = cursor.fetchall()
            for row in result:
                print("After modification of movies table: ", row)
except Error as err:
    print("database connection error: ", err)

# "As shown in the output, the collection_in_mil attribute is now of type DECIMAL(4,1). Also note that in the code
# above, you call cursor.execute() twice. But cursor.fetchall() fetches rows from only the last executed query, which
# is the show_table_query.
#
# Deleting Tables Using the DROP Statement
# To delete a table, you need to execute the DROP TABLE statement in MySQL. Deleting a table is an irreversible
# process. If you execute the code below, then you’ll need to call the CREATE TABLE query again to use the ratings
# table in the upcoming sections.
# To delete the ratings table, send drop_table_query to cursor.execute():
#
# drop_table_query = "DROP TABLE ratings"
# with connection.cursor() as cursor:
#     cursor.execute(drop_table_query)
# If you execute the above code, you will have successfully deleted the ratings table."

# "Inserting Records in Tables
# In the last section, you created three tables in your database: movies, reviewers, and ratings. Now you need to
# populate these tables with data. This section will cover two different ways to insert records in the MySQL Connector
# for Python.
#
# The first method, .execute(), works well when the number of records is small and the records can be hard-coded.
# The second method, .executemany(), is more popular and is better suited for real-world scenarios.
#
# Using .execute()
# The first approach uses the same cursor.execute() method that you’ve been using until now. You write
# the INSERT INTO query in a string and pass it to cursor.execute(). You can use this method to insert data into
# the movies table.
# For reference, the movies table has five attributes: id, title, release_year, genre and collection_in_mil
# You don’t need to add data for id as the AUTO_INCREMENT automatically calculates id for you. The following script
# inserts records into the movies table:
#
try:
    with connect(
        host="localhost",
        user="hector",
        password="saibaba0",
        database="online_movie_rating"
    ) as db_connection:
        insert_movies_query = """
            INSERT INTO movies (title, release_year, genre, collection_in_mil)
            VALUES
                ("Forrest Gump", 1994, "Drama", 330.2),
                ("3 Idiots", 2009, "Drama", 2.4),
                ("Eternal Sunshine of the Spotless Mind", 2004, "Drama", 34.5),
                ("Good Will Hunting", 1997, "Drama", 138.1),
                ("Skyfall", 2012, "Action", 304.6),
                ("Gladiator", 2000, "Action", 188.7),
                ("Black", 2005, "Drama", 3.0),
                ("Titanic", 1997, "Romance", 659.2),
                ("The Shawshank Redemption", 1994, "Drama",28.4),
                ("Udaan", 2010, "Drama", 1.5),
                ("Home Alone", 1990, "Comedy", 286.9),
                ("Casablanca", 1942, "Romance", 1.0),
                ("Avengers: Endgame", 2019, "Action", 858.8),
                ("Night of the Living Dead", 1968, "Horror", 2.5),
                ("The Godfather", 1972, "Crime", 135.6),
                ("Haider", 2014, "Action", 4.2),
                ("Inception", 2010, "Adventure", 293.7),
                ("Evil", 2003, "Horror", 1.3),
                ("Toy Story 4", 2019, "Animation", 434.9),
                ("Air Force One", 1997, "Drama", 138.1),
                ("The Dark Knight", 2008, "Action",535.4),
                ("Bhaag Milkha Bhaag", 2013, "Sport", 4.1),
                ("The Lion King", 1994, "Animation", 423.6),
                ("Pulp Fiction", 1994, "Crime", 108.8),
                ("Kai Po Che", 2013, "Sport", 6.0),
                ("Beasts of No Nation", 2015, "War", 1.4),
                ("Andadhun", 2018, "Thriller", 2.9),
                ("The Silence of the Lambs", 1991, "Crime", 68.2),
                ("Deadpool", 2016, "Action", 363.6),
                ("Drishyam", 2015, "Mystery", 3.0)
            """
        with db_connection.cursor() as cursor:
            cursor.execute(insert_movies_query)
            db_connection.commit()
            print("** successful inserted movies")
except Error as err:
    print("database connection error: ", err)

# "The movies table is now loaded with thirty records. The code calls connection.commit() at the end. It’s crucial
# to call .commit() after preforming any modifications to a table.
#
# Using .executemany()
# The previous approach is more suitable when the number of records is fairly small and you can write these records
# directly into the code. But this is rarely true. You’ll often have this data stored in some other file, or the data
# will be generated by a different script and will need to be added to the MySQL database.
#
# This is where .executemany() comes in handy. It accepts two parameters:
#       A query that contains placeholders for the records that need to be inserted
#       A list that contains all records that you wish to insert
# The following example inserts records for the reviewers table:"
try:
    with connect(
        host="localhost",
        user="hector",
        password="saibaba0",
        database="online_movie_rating"
    ) as db_connection_special:
        insert_reviewers_query = """
            INSERT INTO reviewers
            (first_name, last_name)
            VALUES (%s, %s)        
        """
        reviewers_records = [
            ("Chaitanya", "Baweja"),
            ("Mary", "Cooper"),
            ("John", "Wayne"),
            ("Thomas", "Stoneman"),
            ("Penny", "Hofstadter"),
            ("Mitchell", "Marsh"),
            ("Wyatt", "Skaggs"),
            ("Andre", "Veiga"),
            ("Sheldon", "Cooper"),
            ("Kimbra", "Masters"),
            ("Kat", "Dennings"),
            ("Bruce", "Wayne"),
            ("Domingo", "Cortes"),
            ("Rajesh", "Koothrappali"),
            ("Ben", "Glocker"),
            ("Mahinder", "Dhoni"),
            ("Akbar", "Khan"),
            ("Howard", "Wolowitz"),
            ("Pinkie", "Petit"),
            ("Gurkaran", "Singh"),
            ("Amy", "Farah Fowler"),
            ("Marlon", "Crafford")
        ]
        with db_connection_special.cursor() as cursor:
            cursor.executemany(insert_reviewers_query, reviewers_records)
            db_connection_special.commit()
            print("** successful inserted reviewers")
except Error as err:
    print("database connection error: ", err)

# "In the script above, you pass both the query and the list of records as arguments to .executemany(). These records
# could have been fetched from a file or from the user and stored in the reviewers_records list.
#
# The code uses %s as a placeholder for the two strings that had to be inserted in the insert_reviewers_query.
# Placeholders act as format specifiers and help reserve a spot for a variable inside a string. The specified variable
# is then added to this spot during execution.
#
# You can similarly use .executemany() to insert records in the ratings table:
try:
    with connect(
        host="localhost",
        user="hector",
        password="saibaba0",
        database="online_movie_rating"
    ) as db_connection:
        insert_rating_query = """
            INSERT INTO ratings
            (rating, movie_id, reviewer_id)
            VALUES (%s, %s, %s)
        """
        ratings_records = [
            (6.4, 17, 5), (5.6, 19, 1), (6.3, 22, 14), (5.1, 21, 17),
            (5.0, 5, 5), (6.5, 21, 5), (8.5, 30, 13), (9.7, 6, 4),
            (8.5, 24, 12), (9.9, 14, 9), (8.7, 26, 14), (9.9, 6, 10),
            (5.1, 30, 6), (5.4, 18, 16), (6.2, 6, 20), (7.3, 21, 19),
            (8.1, 17, 18), (5.0, 7, 2), (9.8, 23, 3), (8.0, 22, 9),
            (8.5, 11, 13), (5.0, 5, 11), (5.7, 8, 2), (7.6, 25, 19),
            (5.2, 18, 15), (9.7, 13, 3), (5.8, 18, 8), (5.8, 30, 15),
            (8.4, 21, 18), (6.2, 23, 16), (7.0, 10, 18), (9.5, 30, 20),
            (8.9, 3, 19), (6.4, 12, 2), (7.8, 12, 22), (9.9, 15, 13),
            (7.5, 20, 17), (9.0, 25, 6), (8.5, 23, 2), (5.3, 30, 17),
            (6.4, 5, 10), (8.1, 5, 21), (5.7, 22, 1), (6.3, 28, 4),
            (9.8, 13, 1)
        ]
        with db_connection.cursor() as cursor:
            cursor.executemany(insert_rating_query, ratings_records)
            db_connection.commit()
            print("** successful inserted ratings")
except Error as err:
    print("database connection error: ", err)