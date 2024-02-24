# CareerCompass
This application is designed for currently enrolled students and recent graduates, offering a platform akin to LinkedIn but focused on entry-level job seekers. Recruiters can post job openings and events, while users can connect, message, create posts, and engage with communities aligned with their interests or career goals.

# Dependencies
- PostgreSQL [https://www.postgresql.org/download/]
- Django 
- Psycopg2

# File Structure
CareerCompass/
│
├── env/
│   ├── (virtual environment files)
│
└── careercompass/
    ├── careercompassapp/
    │   ├── __init__.py
    │   ├── settings.py
    │   └── (other Django project files)
    │
    └── careercompassdb/
        ├── migrations/
        │   └── (Django migrations files)
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── models.py
        └── (other Django app files)

- env/: This directory contains the virtual environment created using the python -m venv env command. It typically includes Python executable, libraries, and other necessary files for the environment.

- careercompass/: This is the main directory of your Django project.

- careercompassapp/: This directory represents your Django project (careercompassapp is just a placeholder name). It contains your project-level files such as settings.py, urls.py, wsgi.py, etc.

- settings.py: This file contains your Django project settings, including installed apps and database credentials.
careercompassdb/: This directory represents a Django app within your project (careercompassdb is just a placeholder name). It contains your app-specific files, such as models, views, migrations, etc.

- models.py: This file contains the Django models for your database tables, where you define your database schema using Django's ORM (Object-Relational Mapping).

- migrations/: This directory contains Django migration files generated when you run python manage.py makemigrations. These files manage changes to your database schema over time.

- Other Django app files: These include files such as admin.py, apps.py, views.py, tests.py, etc., depending on what functionality your app requires.

# How to Work on the Project
1. Once you have set your terminals current directory to the repository's location, run the following command to activate the virtual environment in VSCode: `env/Scripts/activate`
2. Run the following command to install all requirements: `pip install -r requirements.txt`
3. Open `pgAdmin4` on your local device and navigate to server and choose PostgreSQL on the hierarchy found on the left side of the window.
4. Right-click on `Databases` and create a new database with a name of your choosing (the current configuration is preset with the database name `careercompassdb`). 
5. Next, navigate to `settings.py`, found in `/careercompass/careercompassapp/` and change the `NAME`, `USER`, `PASSWORD`, `HOST`, and `PORT` firlds under `DATABASES` as needed:
  - NAME → Database name e.g. dbtest previously created in pgAdmin
  - USER → Database username (default is postgres)
  - PASSWORD → Database password
  - HOST → Database host (In development stage, use localhost or IP Address 127.0.0.1 also available)
  - PORT → The port that used to run the database (Default port is 5432)
6. Now, you should be able to make any changes to this project.