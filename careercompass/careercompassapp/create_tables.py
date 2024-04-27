from django.db import connection

# Creates user table with userID primary key and checks if the email is of the correct format
def create_users_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                UserID VARCHAR(20) PRIMARY KEY,
                FirstName VARCHAR(20) NOT NULL,
                LastName VARCHAR(20) NOT NULL,
                PasswordHash VARCHAR(128) NOT NULL,
                AboutMe TEXT,
                Email VARCHAR(63) UNIQUE NOT NULL,
                CHECK (Email LIKE '%@%.%')
            );
        """)

# Creates recruiters table as a child of users - primary key references users and deletes/updates when users is modified
def create_recruiters_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Recruiters (
                UserID VARCHAR(20) PRIMARY KEY REFERENCES Users ON DELETE 
                CASCADE ON UPDATE CASCADE,
                CompanyName VARCHAR(48) NOT NULL,
                AboutCompany TEXT,
                Title VARCHAR(40) NOT NULL
            );
        """)

# Creates students table as a child of users - primary key references users and deletes/updates when users is modified
# Checks if GPA falls between 0 and 4 before inserting/updating
def create_students_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Students (
                UserID VARCHAR(20) PRIMARY KEY REFERENCES Users ON DELETE 
                CASCADE ON UPDATE CASCADE,
                University VARCHAR(60) NOT NULL,
                Degree VARCHAR(48) NOT NULL,
                CurrentYear VARCHAR(9) NOT NULL,
                ExpectedGraduation DATE NOT NULL,
                GPA NUMERIC(3, 2),
                OpenToWork VARCHAR(3),
                CHECK (GPA <= 4.0 AND GPA >= 0.0)
            );
        """)

# Creates posts table where the primary key is the foreign key of the user who posted it and the primary key is the userid and the date posted.
# All posts by a user are deleted/updated if the users ID is deleted/updated
def create_posts_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Posts (
                PostedBy VARCHAR(20) REFERENCES Users ON DELETE CASCADE ON 
                UPDATE CASCADE,
                DatePosted TIMESTAMP,
                Title VARCHAR(36),
                BodyText TEXT,
                Field VARCHAR(20),
                CONSTRAINT post_pk PRIMARY KEY (PostedBy, DatePosted)
            );
        """)

# Creates relationship for likes, where a user from users likes a post from posts. Deleting a user or post will cause the corresponding likes to be deleted
def create_likes_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Likes (
                UserID VARCHAR(20) REFERENCES Users ON DELETE CASCADE ON 
                UPDATE CASCADE,
                PostedBy VARCHAR(20),
                DatePosted TIMESTAMP,
                CONSTRAINT like_pk PRIMARY KEY (UserID, PostedBy, DatePosted),
                CONSTRAINT post_fk FOREIGN KEY (PostedBy, DatePosted) 
                REFERENCES Posts (PostedBy, DatePosted) ON DELETE CASCADE
            );
        """)

# Creates a table for the relationship between users where one user follows another. 
# Deleting a user account will delete the corresponding followers and following relationships stored.
def create_followers_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Followers (
                UserID VARCHAR(20) REFERENCES Users ON DELETE CASCADE ON 
                UPDATE CASCADE,
                FollowerID VARCHAR(20) REFERENCES Users ON DELETE CASCADE ON 
                UPDATE CASCADE,
                CONSTRAINT follower_pk PRIMARY KEY (UserID, FollowerID)      
            );
        """)

