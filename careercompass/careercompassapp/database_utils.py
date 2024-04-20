
# This file contains all database querying functions

from django.db import connection

# Add the user to the database
def add_user(UserID, FirstName, LastName, PhoneNumber, PasswordHash, DOB, Email, Type, AboutMe=None):
     with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """,
            [UserID, FirstName, LastName, PhoneNumber, PasswordHash, DOB, AboutMe, Email]
        )

def add_student(UserID, University, Degree, CurrentYear, ExpectedGraduation, GPA, OpenToWork):
     with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            INSERT INTO students VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            [UserID, University, Degree, CurrentYear, ExpectedGraduation, GPA, OpenToWork]
        )

def add_recruiter(UserID, CompanyName, AboutCompany, Position, CompanyLink):
     with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            INSERT INTO recruiters VALUES (%s, %s, %s, %s, %s);
            """,
            [UserID, CompanyName, AboutCompany, Position, CompanyLink]
        ) 

# Get the user information from the database
def get_user(UserID):
     with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            SELECT * FROM users WHERE users.UserID = %s;
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
            SELECT * FROM students JOIN users 
            ON students.UserID = users.UserID 
            WHERE users.UserID = %s;
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
            SELECT * FROM recruiters JOIN users 
            ON recruiters.UserID = users.UserID 
            WHERE users.UserID = %s;
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
            SELECT COUNT(*) FROM followers WHERE followers.UserID = %s;
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
            SELECT COUNT(*) FROM followers WHERE followers.FollowerID = %s;
            """,
            [UserID]
        )
        # Fetch the row with the correct UserID
        following = cursor.fetchone()
        if following:
            return following
        else:
            return None
        
def create_post(PostedBy, Title, BodyText, Field, Link=None):
    with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            INSERT INTO posts VALUES (%s, NOW(), %s, %s, %s, %s);
            """,
            [PostedBy, Title, BodyText, Field, Link]
        )

def follow(UserID, FollowerID):
    with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            INSERT INTO followers VALUES (%s, %s);
            """,
            [UserID, FollowerID]
        )

def unfollow(UserID, FollowerID):
    with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            DELETE FROM followers WHERE UserID=%s AND FollowerID=%s;
            """,
            [UserID, FollowerID]
        )

def liked(UserID, PostedBy, DatePosted):
    with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            INSERT INTO likes VALUES (%s, %s, %s);
            """,
            [UserID, PostedBy, DatePosted]
        )

def unlike(UserID, PostedBy, DatePosted):
    with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            DELETE FROM likes WHERE UserID=%s AND PostedBy=%s AND DatePosted=%s;
            """,
            [UserID, PostedBy, DatePosted]
        )

def following_list(UserID):
    with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            SELECT UserID FROM followers WHERE FollowerID=%s;
            """,
            [UserID]
        )
        following = cursor.fetchall()
        print(following)
        if following:
            return [item[0] for item in following]
        else:
            return None

def get_user_type(UserID):
    with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            SELECT 
            CASE 
                WHEN EXISTS (SELECT UserID FROM recruiters WHERE UserID=%s) THEN 'R'
                ELSE 'S'
            END;
            """,
            [UserID]
        )
        user_type = cursor.fetchone()
        
        print(user_type)
        if user_type:
            return user_type
        else:
            return None
        