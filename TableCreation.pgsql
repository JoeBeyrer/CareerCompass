CREATE TABLE users (
    UserID VARCHAR(15) PRIMARY KEY,
    FirstName VARCHAR(20),
    LastName VARCHAR(20),
    PhoneNumber CHAR(10),
    PasswordHash VARCHAR(127),
    DOB DATE,
    AboutMe TEXT,
    Email VARCHAR(63)
);


