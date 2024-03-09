
# This file contains all database querying functions

from django.db import connection

# Add the user to the database
def add_user(UserID, FirstName, LastName, PhoneNumber, PasswordHash, DOB, Email, AboutMe=None):
     with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            INSERT INTO careercompassapp_users VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """,
            [UserID, FirstName, LastName, PhoneNumber, PasswordHash, DOB, AboutMe, Email]
        )

# Get the user information from the database
def get_user(UserID):
     with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            SELECT * FROM careercompassapp_users WHERE careercompassapp_users."UserID" = %s;
            """,
            [UserID]
        )
        # Fetch the row with the correct UserID
        user_data = cursor.fetchone()
        if user_data:
            return user_data
        else:
            return None