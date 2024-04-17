
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

def add_student(UserID, University, Degree, CurrentYear, ExpectedGraduation, GPA, OpenToWork):
     with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            INSERT INTO careercompassapp_students VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            [UserID, University, Degree, CurrentYear, ExpectedGraduation, GPA, OpenToWork]
        )

def add_recruiter(UserID, CompanyName, AboutCompany, Position, CompanyLink):
     with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            INSERT INTO careercompassapp_recruiters VALUES (%s, %s, %s, %s, %s);
            """,
            [UserID, CompanyName, AboutCompany, Position, CompanyLink]
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

def get_student_data(UserID):
    with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            SELECT * FROM careercompassapp_students JOIN careercompassapp_users 
            ON careercompassapp_students."UserID_id" = careercompassapp_users."UserID" 
            WHERE careercompassapp_users."UserID" = %s;
            """,
            [UserID]
        )
        # Fetch the row with the correct UserID
        student_data = cursor.fetchone()
        print(student_data)
        if student_data:
            return student_data
        else:
            return None

def get_recruiter_data(UserID):
    with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            SELECT * FROM careercompassapp_recruiters JOIN careercompassapp_users 
            ON careercompassapp_recruiters."UserID_id" = careercompassapp_users."UserID" 
            WHERE careercompassapp_users."UserID" = %s;
            """,
            [UserID]
        )
        # Fetch the row with the correct UserID
        recruiter_data = cursor.fetchone()
        print(recruiter_data)
        if recruiter_data:
            return recruiter_data
        else:
            return None

def get_follower_count(UserID):
    with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            SELECT COUNT(*) FROM careercompassapp_followers WHERE careercompassapp_followers."UserID_id" = %s;
            """,
            [UserID]
        )
        # Fetch the row with the correct UserID
        followers = cursor.fetchone()
        print(followers)
        if followers:
            return followers
        else:
            return None

def get_following_count(UserID):
    with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            SELECT COUNT(*) FROM careercompassapp_followers WHERE careercompassapp_followers."FollowerID_id" = %s;
            """,
            [UserID]
        )
        # Fetch the row with the correct UserID
        following = cursor.fetchone()
        print(following)
        if following:
            return following
        else:
            return None
        
def create_post(PostID, PostedBy, Title, BodyText, Field, Link=None):
    with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            INSERT INTO careercompassapp_posts VALUES (%s, %s, %s, %s, %s, NOW(), %s);
            """,
            [PostID, PostedBy, Title, BodyText, Field, Link]
        )

def follow(UserID, FollowerID):
    with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            INSERT INTO careercompassapp_followers VALUES ('UserID_id'=%s, 'FollowerID_id'=%s);
            """,
            [UserID, FollowerID]
        )

def unfollow(UserID, FollowerID):
    with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            DELETE FROM careercompassapp_followers WHERE 'UserID_id'=%s AND 'FollowerID_id'=%s;
            """,
            [UserID, FollowerID]
        )

def liked(UserID, PostID):
    with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            INSERT INTO careercompassapp_likes VALUES (%s, %s);
            """,
            [UserID, PostID]
        )

def unlike(UserID, PostID):
    with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            DELETE FROM careercompassapp_likes WHERE 'UserID_id'=%s AND 'PostID_id'=%s;
            """,
            [UserID, PostID]
        )

