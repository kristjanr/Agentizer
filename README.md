# About this project    
This is a service for tourist agencies to manage and message tour guides about an upcoming gig.
It was created during and after the Garage 48 Pärnu 2015 - a hackathon in Estonia.


# Set-up on OS X

* Install Python 3.5
* Install [postgresql app](http://postgresapp.com/)
* `export PATH="$PATH:/Applications/Postgres.app/Contents/Versions/latest/bin"`
* `pip install -r requirements`
* `psql -c "CREATE DATABASE agentizer;"`
* set the correct env variables in the .env file:
    * EMAIL_HOST_USER - gmail username
    * EMAIL_HOST_PASSWORD - [create an app password for gmail](https://security.google.com/settings/security/apppasswords?pli=1)
    * DATABASE_URL
    * MESSENTE_USER - username acquired from [messente.com](http://messente.com/)
    * MESSENTE_PASSWORD - password acquired from [messente.com](http://messente.com/)
* `source .env`
* update the site domain at AgentOrganizer/migrations/sites/0002_initialize_sites.py:13
* `python manage.py migrate`
* `python manage.py collectstatic`
* `python manage.py runserver`
