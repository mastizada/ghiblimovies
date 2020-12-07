# GhibliMovies 🎬
 [![pipeline status](https://gitlab.com/mastizada/ghiblimovies/badges/master/pipeline.svg)](https://gitlab.com/mastizada/ghiblimovies/-/pipelines) 
 [![coverage report](https://gitlab.com/mastizada/ghiblimovies/badges/master/coverage.svg)](https://mastizada.gitlab.io/ghiblimovies/) 

Movie list from Studio Ghibli

---

## Install

### Configuration

The project uses a dotenv configuration file that supports both the `.env` file and environment variables.
Create a configuration file from the template using `cp .env.template .env` command.

The default template is configured for the local development environment.
Edit the `.env` file for changing project settings.

### Local setup
This section is only for native installation, you can ignore it and directly use the "Docker-Compose" section for quick installation and running.

This app uses the `poetry` package manager. You can install `poetry` using the package provided by your OS or by using the `sudo pip install poetry` command.

Use these commands to setup and run the application in your local environment:
```console
poetry install
poetry shell
./manage.py migrate
./manage.py runserver
```

If you need a superuser, create one using the `./manage.py createsuperuser` command.

For background tasks, run the celery instance:
```console
celery -A ghiblimovies worker -l INFO
```

You should also run the celery-beat worker for periodic tasks:
```console
celery -A ghiblimovies beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

Run the project tests using the `./manage.py test` command.

### Docker-Compose

Docker-compose have postgresql, redis and rabbitmq instances ready and will start the web server, celery, and celery-beat services.

Run the project using docker-compose:
```console
docker-compose --env-file .env.template up --build
```

---

&copy; 2020 Emin Mastizada. MIT Licenced.
