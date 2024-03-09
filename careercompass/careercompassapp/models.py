from django.db import models

# Initial creation of the users table to store all user data
class Users(models.Model):
    UserID = models.CharField(max_length=15, primary_key=True) # PRIMARY KEY
    FirstName = models.CharField(max_length=20)
    LastName = models.CharField(max_length=20)
    PhoneNumber = models.CharField(max_length=10) # CHAR(10)
    PasswordHash = models.CharField(max_length=128)
    DOB = models.DateField()
    AboutMe = models.TextField(null=True, blank=True)
    Email = models.CharField(max_length=63) # UNIQUE

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="valid_phone_number",
                check=models.Q(PhoneNumber__regex=r'^[0-9]{10}$'),  # Check if PhoneNumber is a 10-digit number
            ),
            models.UniqueConstraint(
                name="unique_email",
                fields=["Email"],  # Ensure Email is unique
            ),
        ]

# Initial creation of the recruiters table, a subclass and type of user
class Recruiters(models.Model):
    UserID = models.ForeignKey('Users', primary_key=True, on_delete=models.CASCADE) # FOREIGN KEY REFERENCES Users
    CompanyName = models.CharField(max_length=20)
    AboutCompany = models.TextField()
    Position = models.CharField(max_length=20)
    CompanyLink = models.CharField(max_length=255)

# Initial creation of the students table, a subclass and type of user
class Students(models.Model):
    UserID =  models.ForeignKey('Users', primary_key=True, on_delete=models.CASCADE) # FOREIGN KEY REFERENCES Users
    University = models.CharField(max_length=60)
    Degree = models.CharField(max_length=48)
    CurrentYear = models.CharField(max_length=9)
    ExpectedGraduation = models.DateField()
    GPA = models.DecimalField(max_digits=1, decimal_places=1) # NUMERIC(1, 1)
    OpenToWork = models.CharField(max_length=1) # CHAR(1)

# Initial creation of the posts table. Posts are created by users
class Posts(models.Model):
    PostID = models.IntegerField(primary_key=True) # PRIMARY KEY
    PostedBy = models.ForeignKey('Users', on_delete=models.CASCADE)  # FOREIGN KEY REFERENCES Users
    Title = models.CharField(max_length=30)
    BodyText = models.TextField()
    Field = models.CharField(max_length=15)
    DatePosted = models.DateField()
    Link = models.CharField(max_length=255)

# Initial creation of the likes table. A user may like another users post
class Likes(models.Model):
    UserID = models.ForeignKey('Users', on_delete=models.CASCADE) # PRIMARY KEY, FOREIGN KEY REFERENCES Users
    PostID = models.ForeignKey('Posts', on_delete=models.CASCADE, to_field='PostID') # PRIMARY KEY, FOREIGN KEY REFERENCES Posts

    # TODO: Add not null and deletes constraints for all "primary keys" - investigate other methods
    class Meta:
        constraints = [
            models.UniqueConstraint( # Used as a primary key as django does not support multiple primary keys
                name='unique_like_combination',
                fields=['UserID', 'PostID']
            )
        ]

# Initial creation of the followers table. A user may follow another users
class Followers(models.Model):
    UserID = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='followers_as_user') # PRIMARY KEY, FOREIGN KEY REFERENCES Users
    FollowerID = models.ForeignKey('Users', on_delete=models.CASCADE, related_name='followers_as_follower')  # PRIMARY KEY, FOREIGN KEY REFERENCES Users

    # TODO: Add not null and deletes constraints for all "primary keys" - investigate other methods
    class Meta:
        constraints = [
            models.UniqueConstraint( # Used as a primary key as django does not support multiple primary keys
                name='unique_follower_combination',
                fields=['UserID', 'FollowerID']
            )
        ]
