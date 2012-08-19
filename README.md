# Promise.ly

# About

# Features
* Promise feed, where you can create and view promises
* In-house custom logging system for admin to monitor core metrics
* Social sharing via FB post or FB/Twitter share buttons

# Coming soon
* Promise feed filtering based on Facebook friends

# Technologies Used
* Redis
* Celery

# Running locally

1. make sure you have mysql installed with a user called root;
2. make sure you have redis installed;
4. create a local.py file with the following settings:
```
    REDIS_CONNECTION = 'redis://localhost:6379'

    FACEBOOK_APP_ID = 'your_facebook_app_id'
    FACEBOOK_APP_SECRET = 'your_facebook_app_secret'

    # https://docs.djangoproject.com/en/1.4/ref/settings/#email-backend
    EMAIL_HOST_USER = 'username'
    EMAIL_HOST_PASSWORD = 'password'
```
5. run `make run`;

# Running on Heroku

# What it looks like
