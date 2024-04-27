
# This file contains all database querying functions

from django.db import connection

# Add the user to the database
def add_user(UserID, FirstName, LastName, PasswordHash, Email, AboutMe=None):
     with connection.cursor() as cursor:
        # Using cursor.execute with %s fields keeps the query safe from SQL injections
        cursor.execute(
            """
            INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s);
            """,
            [UserID, FirstName, LastName, PasswordHash, AboutMe, Email]
        )

# Add the student to the students table
def add_student(UserID, University, Degree, CurrentYear, ExpectedGraduation, GPA, OpenToWork):
     with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO students VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            [UserID, University, Degree, CurrentYear, ExpectedGraduation, GPA, OpenToWork]
        )

# Add the recruiter to the recruiter table
def add_recruiter(UserID, CompanyName, AboutCompany, Position):
     with connection.cursor() as cursor:       
        cursor.execute(
            """
            INSERT INTO recruiters VALUES (%s, %s, %s, %s);
            """,
            [UserID, CompanyName, AboutCompany, Position]
        ) 

# Get the user information from the database
def get_user(UserID):
     with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM users WHERE users.UserID = %s;
            """,
            [UserID]
        )
        
        user_data = cursor.fetchone()
        if user_data:
            return user_data
        else:
            return None

# Get the students data from both the students and users tables
def get_student_data(UserID):
    with connection.cursor() as cursor: 
        cursor.execute(
            """
            SELECT * FROM students JOIN users 
            ON students.UserID = users.UserID 
            WHERE users.UserID = %s;
            """,
            [UserID]
        )
        
        student_data = cursor.fetchone()
        if student_data:
            return student_data
        else:
            return None

# Get the recruiters data from both the recruiters and users tables
def get_recruiter_data(UserID):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM recruiters JOIN users 
            ON recruiters.UserID = users.UserID 
            WHERE users.UserID = %s;
            """,
            [UserID]
        )
        
        recruiter_data = cursor.fetchone()
        if recruiter_data:
            return recruiter_data
        else:
            return None

# Counts how many times the users ID shows as being followed by another user in the followers database
def get_follower_count(UserID):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(*) FROM followers WHERE followers.UserID = %s;
            """,
            [UserID]
        )
        
        followers = cursor.fetchone()
        if followers:
            return followers
        else:
            return None

# Counts how many times the users ID shows as following another user in the followers database
def get_following_count(UserID):
    with connection.cursor() as cursor:
        
        cursor.execute(
            """
            SELECT COUNT(*) FROM followers WHERE followers.FollowerID = %s;
            """,
            [UserID]
        )
        
        following = cursor.fetchone()
        if following:
            return following
        else:
            return None

# Adds the post to the database with the date posted set to the current timestamp of NOW()        
def create_post(PostedBy, Title, BodyText, Field):
    with connection.cursor() as cursor:
        
        cursor.execute(
            """
            INSERT INTO posts VALUES (%s, NOW(), %s, %s, %s);
            """,
            [PostedBy, Title, BodyText, Field]
        )

# Removes the post from the database using the userID and the timestamp it was posted
def delete_post(PostedBy, DatePosted):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM posts WHERE PostedBy=%s AND DatePosted=%s;
            """,
            [PostedBy, DatePosted]
        )

# Adds the userID and ID of the follower to the database when one user follows another
def follow(UserID, FollowerID):
    with connection.cursor() as cursor:
        
        cursor.execute(
            """
            INSERT INTO followers VALUES (%s, %s);
            """,
            [UserID, FollowerID]
        )

# Removes the follower from the follows database when a user unfollows another
def unfollow(UserID, FollowerID):
    with connection.cursor() as cursor:
        
        cursor.execute(
            """
            DELETE FROM followers WHERE UserID=%s AND FollowerID=%s;
            """,
            [UserID, FollowerID]
        )

# Adds like to likes table using current users ID, the posters ID, and the date the post was made
def liked(UserID, PostedBy, DatePosted):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO likes VALUES (%s, %s, %s);
            """,
            [UserID, PostedBy, DatePosted]
        )

# Removes the like from likes in the event of a user unliking a post
def unlike(UserID, PostedBy, DatePosted):
    with connection.cursor() as cursor:
        
        cursor.execute(
            """
            DELETE FROM likes WHERE UserID=%s AND PostedBy=%s AND DatePosted=%s;
            """,
            [UserID, PostedBy, DatePosted]
        )

# Returns a list of all the userIDs from followers where the user being followed is the input provided
def following_list(UserID):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT UserID FROM followers WHERE FollowerID=%s;
            """,
            [UserID]
        )
        following = cursor.fetchall()
        if following:
            return [item[0] for item in following]
        else:
            return None

# Returns a list of all the userIDs from followers where the user following another is the input provided
def get_user_type(UserID):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT 
            CASE 
                WHEN EXISTS (SELECT UserID FROM recruiters WHERE UserID=%s) 
                THEN 'R'
                ELSE 'S'
            END;
            """,
            [UserID]
        )
        user_type = cursor.fetchone()
        if user_type:
            return user_type
        else:
            return None

# Selects all posts made by a specific user
def get_user_posts(UserID):
    with connection.cursor() as cursor:
        
        cursor.execute(
            """
            SELECT * FROM posts WHERE PostedBy=%s ORDER BY DatePosted DESC;
            """,
            [UserID]
        )
        posts = cursor.fetchall()
        if posts:
            return posts
        else:
            return None

# Selects all posts made by users the current user is following. This is done by joining posts and followers on the followerID
# Only posts within the past year will show.
def get_following_posts(UserID):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM posts JOIN followers ON 
            posts.PostedBy=followers.UserID WHERE followers.FollowerID=%s AND 
            posts.DatePosted BETWEEN NOW() - INTERVAL 
            '1 year' AND NOW() ORDER BY posts.DatePosted DESC;
            """,
            [UserID]
        )
        posts = cursor.fetchall()
        if posts:
            return posts
        else:
            return None

# Returns the number of likes for a specific post 
def get_like_count(PostedBy, DatePosted):
    with connection.cursor() as cursor:
        
        cursor.execute(
            """
            SELECT COUNT(*) FROM likes WHERE PostedBy=%s AND DatePosted=%s;
            """,
            [PostedBy, DatePosted]
        )
        likes = cursor.fetchone()
        if likes:
            return likes
        else:
            return None

# Checks if the current user has already liked a post
def check_liked_post(UserID, PostedBy, DatePosted):
    with connection.cursor() as cursor:
        
        cursor.execute(
            """
            SELECT * FROM likes WHERE UserID=%s AND PostedBy=%s AND DatePosted=%s;
            """,
            [UserID, PostedBy, DatePosted]
        )
        posts = cursor.fetchone()
        if posts:
            return posts
        else:
            return None

# Gets a post using the id of the user who posted it and the timestamp it was posted        
def get_post(PostedBy, DatePosted):
    with connection.cursor() as cursor:
        
        cursor.execute(
            """
            SELECT * FROM posts WHERE PostedBy=%s and DatePosted=%s;
            """,
            [PostedBy, DatePosted]
        )
        post = cursor.fetchone()
        if post:
            return post
        else:
            return None

# Search for a user in users using an input string compared to their userID, first name, and last name.
# Only the 30 results with the shortest UserIDs are returned to ensure the closest match by username
def search_user(input):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT UserID, FirstName, LastName FROM users WHERE LOWER(UserID) 
            LIKE LOWER(%s) OR LOWER(FirstName) LIKE LOWER(%s) OR 
            LOWER(LastName) LIKE LOWER(%s) OR LOWER(FirstName || ' ' || 
            LastName) LIKE LOWER(%s) ORDER BY LENGTH(UserID) LIMIT 30;
            """,
            ['%' + input + '%', input + '%', input + '%', input]
        )
        users = cursor.fetchall()
        if users:
            return users
        else:
            return None

# Retrieves the user data for the followers of a provided user by using a JOIN of followers and users
def get_followers(UserID):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT f.FollowerID, u.FirstName, u.LastName
            FROM followers f JOIN users u ON f.FollowerID=u.UserID
            WHERE f.UserID = %s;
            """,
            [UserID]
        )
        followers = cursor.fetchall()
        if followers:
            return followers
        else:
            return None

# Retrieves the user data for the users followed by the provided user using a JOIN of followers and users
def get_following(UserID):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT f.UserID, u.FirstName, u.LastName
            FROM followers f JOIN users u ON f.UserID=u.UserID
            WHERE f.FollowerID = %s;
            """,
            [UserID]
        )
        following = cursor.fetchall()
        if following:
            return following
        else:
            return None

# Gets the total likes across all posts made by a user
def get_user_likes_count(UserID):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(postedby) FROM likes WHERE likes.postedby = %s;
            """,
            [UserID]
        )
        total_likes = cursor.fetchone()
        if total_likes:
            return total_likes
        else:
            return 0  # Return 0 if no likes found for the user

# Updates user data using casestatements so that not all inputs are required.
# If the input is NULL, we do not change the data, otherwise it is updated to the new value
def update_user(UserID, FirstName, LastName, PasswordHash, AboutMe, Email, current_user):
    with connection.cursor() as cursor:
        UserID = None if UserID == "" else UserID
        FirstName = None if FirstName == "" else FirstName
        LastName = None if LastName == "" else LastName
        PasswordHash = None if PasswordHash == "" else PasswordHash
        AboutMe = None if AboutMe == "" else AboutMe
        Email = None if Email == "" else Email
        cursor.execute(
            """
            UPDATE users 
            SET 
                UserID = CASE WHEN %s IS NOT NULL THEN %s ELSE UserID END,
                FirstName = CASE WHEN %s IS NOT NULL THEN %s ELSE FirstName END,
                LastName = CASE WHEN %s IS NOT NULL THEN %s ELSE LastName END,
                PasswordHash = CASE WHEN %s IS NOT NULL THEN %s ELSE PasswordHash END,
                AboutMe = CASE WHEN %s IS NOT NULL THEN %s ELSE AboutMe END,
                Email = CASE WHEN %s IS NOT NULL THEN %s ELSE Email END
            WHERE UserID = %s;
            """,
            [UserID, UserID, FirstName, FirstName, LastName, LastName, PasswordHash, 
             PasswordHash, AboutMe, AboutMe, 
             Email, Email, current_user]
            
        )

# Updates all student specific data in the students table
def update_student(University, Degree, CurrentYear, ExpectedGraduation, GPA, OpenToWork, current_user):
    with connection.cursor() as cursor:
        University = None if University == "" else University
        Degree = None if Degree == "" else Degree
        CurrentYear = None if CurrentYear == "" else CurrentYear
        ExpectedGraduation = None if ExpectedGraduation == "" else ExpectedGraduation
        GPA = None if GPA == "" else GPA
        OpenToWork = None if OpenToWork == "" else OpenToWork
        cursor.execute(
            """
            UPDATE students 
            SET 
                University = CASE WHEN %s IS NOT NULL THEN %s ELSE University END,
                Degree = CASE WHEN %s IS NOT NULL THEN %s ELSE Degree END,
                CurrentYear = CASE WHEN %s IS NOT NULL THEN %s ELSE CurrentYear END,
                ExpectedGraduation = CASE WHEN %s IS NOT NULL THEN %s ELSE ExpectedGraduation END,
                GPA = CASE WHEN %s IS NOT NULL THEN %s ELSE GPA END,
                OpenToWork = CASE WHEN %s IS NOT NULL THEN %s ELSE OpenToWork END
            WHERE UserID = %s;
            """,
            [University, University, Degree, Degree, CurrentYear, CurrentYear, 
             ExpectedGraduation, ExpectedGraduation, GPA, GPA, OpenToWork, OpenToWork, current_user]

        )

# Updates all recruiter specific data in the recruiters table
def update_recruiter(CompanyName, AboutCompany, Position, current_user):
    with connection.cursor() as cursor:
        CompanyName = None if CompanyName == "" else CompanyName
        AboutCompany = None if AboutCompany == "" else AboutCompany
        Position = None if Position == "" else Position
        cursor.execute(
            """
            UPDATE recruiters 
            SET 
                CompanyName = CASE WHEN %s IS NOT NULL THEN %s ELSE CompanyName END,
                AboutCompany = CASE WHEN %s IS NOT NULL THEN %s ELSE AboutCompany END,
                Title = CASE WHEN %s IS NOT NULL THEN %s ELSE Title END
            WHERE UserID = %s;
            """,
            [CompanyName, CompanyName, AboutCompany, AboutCompany, 
             Position, Position, current_user]
        )

# Checks if the email has already been used by another user for input validation  
def check_email(email):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT Email FROM users WHERE Email=%s;
            """,
            [email]
        )
        email_exists = cursor.fetchone()
        print(email_exists)
        if email_exists != None:
            return True
        else:
            return False  

# Checks if the username already exists in the table for input validation        
def check_username(UserID):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT UserID FROM users WHERE UserID=%s;
            """,
            [UserID]
        )
        UserID_exists = cursor.fetchone()
        if UserID_exists != None:
            return True
        else:
            return False  

# Deletes the users data (cascades) using the userID
def delete_user(UserID):
     with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM users WHERE UserID=%s;
            """,
            [UserID]
        )