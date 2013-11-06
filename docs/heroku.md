# Heroku

## Getting setup to use heroku short version

1. Install Heroku Toolbelt from https://toolbelt.heroku.com/

2. Run `heroku login`

3. Add the remote to your SacredPy Repo
    a. Go into your sacredpy direction
    b. Add the git remote
        ```git remote add heroku git@heroku.com:sacredpy.git```

## Running against the heroku database
1. Export the heroku environment variable
    ```export `heroku config -s --app pytn````

2. Now you can run any command you like. 
	For example:
    ```python manage.py runserver```
