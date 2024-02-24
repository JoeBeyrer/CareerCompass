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
