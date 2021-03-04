""" This is how the user will be able to create any new module with the fields that they want to use. When adding a module you will just
need to use the database name again in order to connect to the database and make a new table. """

import mysql.connector
from configparser import ConfigParser

# Here we are setting up our configparser for our configurations
config_object = ConfigParser()

print("This section is where you will be creating a new database or adding a new table to your program.")
print("")
print("")

# Here is where you want to name it town
print("If you are just setting up your database then you will need to give it a name.")
database_name = input("If you are adding a table to your database, put in the database name that you are adding to? ")

# Here we are finding out which module is being created and then its making the naming convention for the
# config file
module_config = input("Is this your first table or a new table? If this is another table then enter the number of this table. ")
module_naming = "Table" + str(module_config)

# Replaces any spaces for the database name with an _
database_name = database_name.lower()
database_name = database_name.replace(" ", "_")

# Here is where its creating the title of the config file and letting the program know where
# to store it.
title_config = "configs/"+ module_naming + "_table_config.ini"

# Step 1 create the database name if there isn't one

# This section is to make the objects needed to use mySQL
sql_config_object = ConfigParser()
sql_config_object.read('configs\mysqlconfig.ini')

host_config = sql_config_object.get('mysqlconnection', 'host')
sqluser_config = sql_config_object.get('mysqlconnection', 'user')
sqlpass_config = sql_config_object.get('mysqlconnection', 'passwd')


data_connect = mysql.connector.connect(
            host=host_config,
            user=sqluser_config,
            passwd=sqlpass_config
)

my_cursor = data_connect.cursor()

# This will create the table name if it doesn't exist.
query = "CREATE DATABASE IF NOT EXISTS {}".format(database_name)
my_cursor.execute(query)


# Creating the schema config
config_object["schema"] = {
    "schema": database_name
}


# MySQL demands to know which database to use before configuring tables and columns this ensures it goes to it.
query = "USE {}".format(database_name)
my_cursor.execute(query)



# STEP 2 Create the new table with primary key, created column and updated column
# This creates the table name and auto configures primary key, created date, updated date columns.
# These extra columns can come in handy for data analysis.
table_name = input("What do you want to name your table? ")
table_name = table_name.replace(" ", "_")
updatedtable_name = (table_name + "_id")

tableCreation = ("CREATE TABLE {} ({} INT NOT NULL auto_increment PRIMARY KEY, created_date TIMESTAMP default now(),updated_date TIMESTAMP default now() on update now());".format(table_name, updatedtable_name))

# Creating the table name
config_object[module_naming] = {
    "tableName": table_name
}


my_cursor.execute(tableCreation)


# STEP 3 Create the columns
# This section creates two loops. 1) if another_column is less than 0 then it will keep asking if you want to make more columns.
# Depending on the users input it will dictate which command to use to create the appropriate column for the user. When
# the user is ready to commit the configurations it will enact the second loop. 2) this loop will ask if the user is sure
# they want to commit the records. If they say yes then it will change another_column to 2 and end the cycle.


# This variable is the hook that is needed to keep the loop going or to close it. If it stays less than 1 it will stay in the loop
# If it goes to over 1 then it will close the loop and move on with the script
another_column = 0

# This variable helps with the naming convention for the config.ini file.
column_count = 0

# Here is where we are going the loop through the questions to create the columns
# CAN'T HAVE A DATE FIELD AS THE FIRST FIELD THAT IS CREATED. THERE NEEDS TO BE LOGIC PUT
# IN PLACE THAT WILL ENSURE IF IT HAPPENS THEN THE USER SELECTS THE SEARCH FIELD IT WILL GO INFRONT OF IT.

while another_column <= 1:
    # To test the adding column function just make the column configuration default standards
    column_name = input("What is the name of the column? ")
    column_attribute = input("What kind of data is stored in this column? Choose: single, date, date&time, text, number ")

    column_name = column_name.lower()
    column_name = column_name.replace(" ", "_")
    column_attribute = column_attribute.lower()

    if column_attribute == "single":
        query1 = "ALTER TABLE {} ADD {} VARCHAR (100) NULL;".format(table_name, column_name)
        my_cursor.execute(query1)
    elif column_attribute == "date":
        query2 = "ALTER TABLE {} ADD {} DATE NULL;".format(table_name, column_name)
        my_cursor.execute(query2)
    elif column_attribute == "date&time":
        query3 = "ALTER TABLE {} ADD {} DATETIME NULL;".format(table_name, column_name)
        my_cursor.execute(query3)
    elif column_attribute == "text":
        query4 = "ALTER TABLE {} add {} TEXT NULL;".format(table_name, column_name)
        my_cursor.execute(query4)
    elif column_attribute == "number":
        query5 = "ALTER TABLE {} ADD {} DECIMAL (12,2) NULL;".format(table_name, column_name)
        my_cursor.execute(query5)

    # This makes the count into a string
    merge_count = "column" + str(column_count)

    # This is how I am reading and adding to the correct section
    config_tableName = config_object[module_naming]
    config_tableName[merge_count]=column_name

    column_count += 1

    # Here is where we are going to end the script.
    ending_loop = input("Do you want to add another column? yes or no ")
    if ending_loop == "yes":
        another_column = 0
    else:
        another_column = 1

    while another_column == 1:
        confirm = input("If you want to save these changes type yes, if not then type no ")

        if confirm == "yes":
            another_column = 2
        elif confirm == "no":
            another_column = 0


# This is how I am committing all of my configurations that I am creating
with open(title_config, 'w') as conf:
    config_object.write(conf)




