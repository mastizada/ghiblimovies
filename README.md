# GhibliMovies 🎬
 [![pipeline status](https://gitlab.com/mastizada/ghiblimovies/badges/master/pipeline.svg)](https://gitlab.com/mastizada/ghiblimovies/-/commits/master) 
 [![coverage report](https://gitlab.com/mastizada/ghiblimovies/badges/master/coverage.svg)](https://gitlab.com/mastizada/ghiblimovies/-/commits/master) 

Movie list from Studio Ghibli

---

## Install

### Configuration

The project uses a dotenv configuration file that supports both the `.env` file and environment variables.
Create a configuration file from the template using `cp .env.template .env` command.

The default template is configured for the local development environment.
Edit the `.env` file for changing project settings.

### Local setup
This app uses the `poetry` package manager. You can install the package provided by your OS's default package manager or by using the `sudo pip install poetry` command.

Use these commands to setup and run the application in your local environment:

    poetry install
    poetry shell
    cp .env.template .env
    ./manage.py migrate
    ./manage.py runserver

If you need a superuser, create one using the `./manage.py createsuperuser` command.

Run the project tests using the `./manage.py test` command.

---

&copy; 2020 Emin Mastizada. MIT Licenced.
