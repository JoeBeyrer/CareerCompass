from django.db import models

# Initial creation of the users table to store all user data
class Users(models.Model):
    UserID = models.CharField(max_length=15, primary_key=True)
    FirstName = models.CharField(max_length=20)
    LastName = models.CharField(max_length=20)
    PhoneNumber = models.CharField(max_length=10)
    PasswordHash = models.CharField(max_length=127)
    DOB = models.DateField()
    AboutMe = models.TextField()
    Email = models.CharField(max_length=63)

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
            models.CheckConstraint(
                name="min_length_userID",
                check=models.Q(UserID__regex=r'^.{15}$'),  # Check if UserID is 15 characters long
            ),
        ]

class Recruiters(models.Model):
    UserID = models.CharField(max_length=15, primary_key=True) # FOREIGN KEY REFERENCES Users
    CompanyName = models.CharField(max_length=20)
    AboutCompany = models.TextField()
    Position = models.CharField(max_length=20)
    CompanyLink = models.CharField(max_length=255)

class Students(models.Model):
    UserID = models.CharField(max_length=15, primary_key=True) # FOREIGN KEY REFERENCES Users
    University = models.CharField(max_length=60)
    Degree = models.CharField(max_length=48)
    CurrentYear = models.CharField(max_length=9)
    ExpectedGraduation = models.DateField()
    GPA = models.models.DecimalField(max_digits=1, decimal_places=2) # NUMERIC(1, 2)
    OpenToWork = models.CharField(max_length=1) # CHAR(1)

class Posts(models.Model):
    PostID = models.IntegerField() # PRIMARY KEY
    PostedBy = models.CharField(max_length=15) # PRIMARY KEY, FOREIGN KEY REFERENCES Users
    Title = models.CharField(max_length=30)
    BodyText = models.TextField()
    Field = models.CharField(max_length=15)
    DatePosted = models.DateField()
    Link = models.CharField(max_length=255)


class Likes(models.Model):
    UserID = models.CharField(max_length=15) # PRIMARY KEY, FOREIGN KEY REFERENCES Users
    PostID = models.IntegerField() # PRIMARY KEY, FOREIGN KEY REFERENCES Posts
    PostedBy = models.CharField(max_length=15) # PRIMARY KEY, FOREIGN KEY REFERENCES Posts


class Followers(models.Model):
    UserID = models.CharField(max_length=15) # PRIMARY KEY, FOREIGN KEY REFERENCES Users
    FollowerID = models.CharField(max_length=15) # PRIMARY KEY, FOREIGN KEY REFERENCES Users
