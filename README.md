# CareerCompass
This application is designed for currently enrolled students and recent graduates, offering a platform akin to LinkedIn but focused on entry-level job seekers. Recruiters can post job openings and events, while users can connect, create posts, and engage with communities aligned with their interests or career goals.

## Dependencies
- [PostgreSQL](https://www.postgresql.org/download/)
- Django 

## File Structure
- env/: This directory contains the virtual environment created using the python -m venv env command. It includes Python executable, libraries, and other necessary files for the environment.

- `careercompass/`: This is the main directory of the Django project.

- `./careercompass/careercompass/`: This directory represents the Django project. It contains the project-level files such as settings.py, urls.py, wsgi.py, etc.

- `./careercompass/careercompass/settings.py`: This file contains the Django project settings, including installed apps and database credentials.

- `./careercompass/careercompassapp/`: This directory represents the main Django app within the project. It contains the app-specific files, such as models, views, migrations, etc.

- `./careercompass/careercompassapp/models.py`: This file contains the Django models for the PostgreSQL database tables, where we define the database schema using Django's ORM (Object-Relational Mapping).

- `./careercompass/careercompassapp/migrations/`: This directory contains Django migration files generated when running python manage.py makemigrations. These files manage changes to the database schema over time.

- `./careercompass/careercompassapp/database_utils.py`: This file contains functions used to execute raw SQL queries. These functions will be called on certain actions within the `./careercompass/careercompassapp/views.py` file.

- `./careercompass/careercompassapp/views.py`: This file contains the views for the Django app, which handle HTTP requests and responses. It includes logic to interact with the database, process user input, and render HTML templates.

- Other Django app files: These include files such as admin.py, apps.py, tests.py, etc., depending on what functionality the app requires.

## How to Work on the Project
1. Once you have set your terminals current directory to the repository's location, run the following command to activate the virtual environment in VSCode: `env/Scripts/activate`

2. Run the following command to install all requirements: `pip install -r requirements.txt`

3. Open `pgAdmin4` on your local device and navigate to server and choose PostgreSQL on the hierarchy found on the left side of the window.

4. Right-click on `Databases` and create a new database with a name of your choosing (the current configuration is preset with the database name `dbcareercompass`). 

5. Next, navigate to `settings.py`, found in `/careercompass/careercompassapp/` and change the `NAME`, `USER`, `PASSWORD`, `HOST`, and `PORT` firlds under `DATABASES` as needed:
   - NAME → Database name e.g. dbtest previously created in pgAdmin
   - USER → Database username (default is postgres)
   - PASSWORD → Database password
   - HOST → Database host (In development stage, use localhost or IP Address 127.0.0.1 also available)
   - PORT → The port that used to run the database (Default port is 5432)

6. Now, you should be able to make any changes to this project.

## How to Apply Database Schema Changes
1. Set your current directory to `CareerCompass/careercompass`.

2. Run the command: `python manage.py makemigrations`.
   - You should see a list of all the schema changes you made.

3. Run the command: `python manage.py migrate`.
   - You should see a list of the chema changes you made, each followed by an `OK` message.

4. Check your database schema in `pgAdmin4` to make sure the changes have been successfully mad.