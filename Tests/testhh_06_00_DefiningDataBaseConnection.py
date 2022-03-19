# "TIPS for database testing using Selenium.
#   ****** This database example included in the serie of code testhh_06_xx can be found at this website
#   https://realpython.com/python-mysql/
#
# - I have downloaded and installed MySQL software which contains mySQL and others software.
#  keep in mind the port number were mySQL start running. frequently it is 3306.
# - Updated the path environment variable with the directory where the mysql executable is located,
#   this is mySQLPath C:\Program Files\MySQL\MySQL Server 8.0\bin
#
#  - Start the MySQL service by:
#       1- right click on the bottom line and click on the Task Manager Option
#       2- click on the Services tab.
#       3- Select the service MySQL80 and right click on top the stopped status and click on start.
#  This error is generated when MySQL80 service is not started:
#      ERROR 2003 (HY000): Can't connect to MySQL server on 'localhost' (10061)
#
# - Start Program: Open the MySQL meny and click on "MySQL Workbench 6.3 CE"
# - On the INSTANCE section, click on Start/Shutdown to start the database Server.
# - login to mysql with the root user with this command: mysql -u root -p
#   note: -u root is the user name, -p is for the password.
#   these are the userId an password we have defined:
#    root/root or sai..b0 and hector/sai....b0
# - after clicking Enter, will be asking for password, click Enter because there is no password defined
#   for the user root. this is only for practice.
# - Created the testdb database with this command: CREATE DATABASE testdb;
# - To start using the database issue this command: use testdb;
# - Created a table in the database with this command:
#      create table training (name varchar(20), course varchar(20), location varchar(20), skill varchar(20));
# - inserted some rows to the table with command:
#      insert into training values('Venky','Loadrunner','UK','Performance');
#      insert into training values('Venktesh','SoapUI','US','Services');
#      insert into training values('Trainer','Selenium','India','functional');
#      insert into training values('Automation','Qtp','Canada','HPtool');
#
# 					ACCESSING DATABASE DATA USING Pythoh Selenium.
# - After creating the Selenium project,
# - Define the JDBC connection and for this, first, we have to download and configure the .JAR file "
#
# "Many popular programming languages have their own database API. For example, Java has the Java Database Connectivity
# (JDBC) API. If you need to connect a Java application to a MySQL database, then you need to use the MySQL JDBC
# connector, which follows the JDBC API.
#
# Similarly, in Python you need to install a Python MySQL connector to interact with a MySQL database. Many packages
# follow the DB-API standards, but the most popular among them is MySQL Connector/Python. You can get it with pip:
#
# $ pip install mysql-connector-python
# pip installs the connector as a third-party module in the currently active virtual environment. It’s recommended that
# you set up an isolated virtual environment for the project along with all the dependencies.
#
# To test if the installation was successful, type the following command on your Python terminal:
#
# >>> import mysql.connector
# If the above code executes with no errors, then mysql.connector is installed and ready to use. If you encounter any
# errors, then make sure you’re in the correct virtual environment and you’re using the right Python interpreter.
#
# Make sure that you’re installing the correct mysql-connector-python package, which is a pure-Python implementation.
# Beware of similarly named but now depreciated connectors like mysql-connector."
from getpass import getpass

# "Establishing a Connection With MySQL Server
# MySQL is a server-based database management system. One server might contain multiple databases. To interact with
# a database, you must first establish a connection with the server. The general workflow of a Python program that
# interacts with a MySQL-based database is as follows:
#
# Connect to the MySQL server.
# Create a new database.
# Connect to the newly created or an existing database.
# Execute a SQL query and fetch results.
# Inform the database if any changes are made to a table.
# Close the connection to the MySQL server.
# This is a generic workflow that might vary depending on the individual application. But whatever the application might be, the first step is to connect your database with your application.
#
# Establishing a Connection
# The first step in interacting with a MySQL server is to establish a connection. To do this, you need connect() from
# the mysql.connector module. This function takes in parameters like host, user, and password and returns a
# MySQLConnection object. You can receive these credentials as input from the user and pass them to connect():"
from mysql.connector import connect, Error

        # try:
        #     with connect(
        #         host = "localhost",
        #         # user = input("Enter usernameDB: "),
        #         user = "hector",
        #         password = getpass("Enter pasword: "),
        #     ) as db_connection:
        #         print("The DB connection is: ", db_connection)
        # except Error as err:
        #     print("The DB connection error is: ", err)

# "The code above uses the entered login credentials to establish a connection with your MySQL server. In return,
# you get a MySQLConnection object, which is stored in the connection variable. From now on, you’ll use this variable
# to access your MySQL server.
# There are several important things to notice in the code above:
#
# You should always deal with the exceptions that might be raised while establishing a connection to the MySQL server.
# This is why you use a try … except block to catch and print any exceptions that you might encounter.
#
# You should always close the connection after you’re done accessing the database. Leaving unused open connections can
# lead to several unexpected errors and performance issues. The above code takes advantage of a context manager
# using with, which abstracts away the connection cleanup process.
# You should never hard-code your login credentials, that is, your username and password, directly in a Python script.
# This is a bad practice for deployment and poses a serious security threat. The code above prompts the user for login
# credentials. It uses the built-in getpass module to hide the password. While this is better than hard-coding, there
# are other, more secure ways to store sensitive information, like using environment variables.
#
# You’ve now established a connection between your program and your MySQL server, but you still need to either create
# a new database or connect to an existing database inside the server.
# Creating a New Database"
# In the last section, you established a connection with your MySQL server. To create a new database, you need to
# execute a SQL statement:
#           CREATE DATABASE books_db;
# "The above statement will create a new database with the name books_db.
#
# Note: In MySQL, it’s mandatory to put a semicolon (;) at the end of a statement, which denotes the termination of
# a query. However, MySQL Connector/Python automatically appends a semicolon at the end of your queries, so there’s
# no need to use it in your Python code.
#
# To execute a SQL query in Python, you’ll need to use a cursor, which abstracts away the access to database records.
# MySQL Connector/Python provides you with the MySQLCursor class, which instantiates objects that can execute
# MySQL queries in Python. An instance of the MySQLCursor class is also called a cursor.
#
# cursor objects make use of a MySQLConnection object to interact with your MySQL server. To create a cursor, use the
# '.cursor()' method of your connection variable:"

        #cursor = db_connection.cursor()

# "The above code gives you an instance of the MySQLCursor class.
# A query that needs to be executed is sent to cursor.execute() in string format. In this particular occasion,
# you’ll send the CREATE DATABASE query to cursor.execute():

try:
    with connect(
        host="localhost",
        # user=input("Enter user name:"),
        user="hector",
        # password=getpass("Enter password: ")
        password="saibaba0"
    ) as db_connection:
        create_db_query = "CREATE DATABASE online_movie_rating"
        with db_connection.cursor() as my_cursor:
            my_cursor.execute(create_db_query)
except Error as err:
    print("The DB Connection or Query error is: ", err)

# "After executing of the code above, you’ll have a new database called online_movie_rating in your MySQL server.
#
# The CREATE DATABASE query is stored as a string in the create_db_query variable and then passed to cursor.execute()
# for execution. The code uses a context manager 'WITH' with the cursor object to handle the cleanup process.
#
# You might receive an error here if a database with the same name already exists in your server. To confirm this,
# you can display the name of all databases in your server. Using the same MySQLConnection (db_connection) object
# from earlier, execute the SHOW DATABASES statement:"
show_db_query = "SHOW DATABASES"
with db_connection.cursor() as my_cursor:
    my_cursor.execute(show_db_query)
    for row_returned in my_cursor:   # my_cursor contains all the rows returned by the query, as a tuple
        print("database in server: ", row_returned)

# "The above code prints the names of all the databases currently in your MySQL server. The SHOW DATABASES command
# also outputs some databases that you didn’t create in your server, like information_schema, performance_schema,
# and so on. These databases are generated automatically by the MySQL server and provide access to a variety of
# database metadata and MySQL server settings.
#
# You created a new database in this section by executing the CREATE DATABASE statement. In the next section,
# you’ll see how to connect to a database that already exists.
#
# "