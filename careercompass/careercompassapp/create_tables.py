from django.db import connection

def create_users_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                UserID VARCHAR(20) PRIMARY KEY,
                FirstName VARCHAR(20) NOT NULL,
                LastName VARCHAR(20) NOT NULL,
                PasswordHash VARCHAR(128) NOT NULL,
                AboutMe TEXT,
                Email VARCHAR(63) UNIQUE NOT NULL
            );
        """)

def create_recruiters_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Recruiters (
                UserID VARCHAR(20) PRIMARY KEY REFERENCES Users ON DELETE CASCADE ON UPDATE CASCADE,
                CompanyName VARCHAR(48) NOT NULL,
                AboutCompany TEXT,
                Title VARCHAR(40) NOT NULL
            );
        """)

def create_students_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Students (
                UserID VARCHAR(20) PRIMARY KEY REFERENCES Users ON DELETE CASCADE ON UPDATE CASCADE,
                University VARCHAR(60) NOT NULL,
                Degree VARCHAR(48) NOT NULL,
                CurrentYear VARCHAR(9) NOT NULL,
                ExpectedGraduation DATE NOT NULL,
                GPA NUMERIC(3, 2),
                OpenToWork VARCHAR(3)
            );
        """)


def create_posts_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Posts (
                PostedBy VARCHAR(20) REFERENCES Users ON DELETE CASCADE ON UPDATE CASCADE,
                DatePosted TIMESTAMP,
                Title VARCHAR(36),
                BodyText TEXT,
                Field VARCHAR(20),
                CONSTRAINT post_pk PRIMARY KEY (PostedBy, DatePosted)
            );
        """)

def create_likes_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Likes (
                UserID VARCHAR(20) REFERENCES Users ON DELETE CASCADE ON UPDATE CASCADE,
                PostedBy VARCHAR(15),
                DatePosted TIMESTAMP,
                CONSTRAINT like_pk PRIMARY KEY (UserID, PostedBy, DatePosted),
                CONSTRAINT post_fk FOREIGN KEY (PostedBy, DatePosted) REFERENCES 
                Posts (PostedBy, DatePosted) ON DELETE CASCADE ON UPDATE CASCADE
            );
        """)

def create_followers_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Followers (
                UserID VARCHAR(20) REFERENCES Users ON DELETE CASCADE ON UPDATE CASCADE,
                FollowerID VARCHAR(20) REFERENCES Users ON DELETE CASCADE ON UPDATE CASCADE,
                CONSTRAINT follower_pk PRIMARY KEY (UserID, FollowerID)      
            );
        """)

