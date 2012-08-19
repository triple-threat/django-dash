# Promise.ly

# About

At http://promise.ly you are able to create promises and share them with your friends so they can support you untill you achieve your goal.
When the deadline of your promise is near, you will be notified so you can validate if you achieved your goal or not.
Promise.ly uses facebook, so your activies can be shared to your facebook friends automatically.


# Features
* Promise feed, where you can create and view promises
* Promise feed filtering based on Facebook friends, your own promises,  and promises you support
* Custom logging system for admin to monitor core metrics
* Social sharing via FB post or FB/Twitter share buttons


# Technologies Used
* Redis
* Postgres
* Django-facebook

# Python requirements


# How to run it locally

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
5. run `make run`

# What it looks like
