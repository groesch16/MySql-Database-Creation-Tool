# This script will help you set up your configuration file to access your database after you install mysql. You will only have to do this once.
# The rest of the software will use this config file generated in the config directory to access your mysql installation.
from configparser import ConfigParser

access_object = ConfigParser()

computer_name = input("Where is the database being hosted? ")
user_name = input("What is the username to access your schema? ")
pass_word = input("What is the password to authenticate into your schema? ")

access_object['mysqlconnection'] = {
    'host': computer_name,
    'user': user_name,
    'passwd': pass_word
}

with open('configs\mysqlconfig.ini','w') as configfile:
    access_object.write(configfile)
