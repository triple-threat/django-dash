# Promise.ly

# About

At http://promise.ly, you make promises and get friends to support you so that you are able to achieve them. Likewise, you can support your friends in their endeavors through the promises they make. Also, share these promises through Facebook and Twitter to get your friends' support!
When the deadline of your promise is near, you will be notified so you can validate if you achieved your goal or not.


# Features
* Create promises
* View promises on the promise feed
* Filter promise feed by your promises, your supported promises, your friends' promises
* Monitor core metrics through a custom metrics logging system, powered by Redis
* Share your promises and the promises you support via Facebook and Twitter
* Enter promises using natural language, since the form uses naive natural language processing, i.e. it parses '2 weeks' from 'I want to learn yoga in 2 weeks' to autopopulate the deadline select fields in the form.
* Receive email notifications through the custom email engine when you get a supporter or a comment or when the deadline is near, you get a reminder.

# Technologies Used
* Redis for powering metrics logging and storing often accessed data like a user's promises and which promises the user supports.
* Postgres
* Django-facebook for facebook auth and posting
* Heroku chronograph for email notifications and promise expiration
* Less
* Highcharts JS for metric analytics display
* Twitter Bootstrap

# How to run it locally

1. make sure you have mysql installed with a user called root;
2. make sure you have redis installed;
3. create a local.py file inside the settings folder with the following settings:
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
Check it out at http://promise.ly!