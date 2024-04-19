from django.db import connection

def create_users_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                UserID VARCHAR(15) PRIMARY KEY,
                FirstName VARCHAR(20) NOT NULL,
                LastName VARCHAR(20) NOT NULL,
                PhoneNumber CHAR(10) NOT NULL,
                PasswordHash VARCHAR(128) NOT NULL,
                DOB DATE NOT NULL,
                AboutMe TEXT,
                Email VARCHAR(63) UNIQUE NOT NULL
            );
        """)

def create_recruiters_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Recruiters (
                UserID VARCHAR(15) PRIMARY KEY REFERENCES Users,
                CompanyName VARCHAR(20) NOT NULL,
                AboutCompany TEXT,
                Title VARCHAR(20) NOT NULL,
                CompanyLink CHAR(255)
            );
        """)

def create_students_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Students (
                UserID VARCHAR(15) PRIMARY KEY REFERENCES Users,
                University VARCHAR(60) NOT NULL,
                Degree VARCHAR(48) NOT NULL,
                CurrentYear CHAR(9) NOT NULL,
                ExpectedGraduation DATE NOT NULL,
                GPA NUMERIC(3, 2),
                OpenToWork VARCHAR(3)
            );
        """)


def create_posts_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Posts (
                PostedBy VARCHAR(15) REFERENCES Users,
                DatePosted TIMESTAMP,
                Title VARCHAR(30),
                BodyText TEXT,
                Field VARCHAR(20),
                Link VARCHAR(255),
                CONSTRAINT post_pk PRIMARY KEY (PostedBy, DatePosted)
            );
        """)

def create_likes_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Likes (
                UserID VARCHAR(15) REFERENCES Users,
                PostedBy VARCHAR(15),
                DatePosted TIMESTAMP,
                CONSTRAINT like_pk PRIMARY KEY (UserID, PostedBy, DatePosted),
                CONSTRAINT post_fk FOREIGN KEY (PostedBy, DatePosted) REFERENCES 
                Posts (PostedBy, DatePosted)
            );
        """)

def create_followers_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Followers (
                UserID VARCHAR(15) REFERENCES Users,
                FollowerID VARCHAR(15) REFERENCES Users,
                CONSTRAINT follower_pk PRIMARY KEY (UserID, FollowerID)      
            );
        """)

