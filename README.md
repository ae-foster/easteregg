# eEaster Egg Hunt

This repo supports the eEaster Egg Hunt run by me (Adam Foster), Tom Flynn, Matt John, Tim Foster
 and others.
 
The website is currently hosted at https://eeasteregg.herokuapp.com/egghunt/

## Contribution workflow

0. Make a new feature branch, based on `staging`
0. Make your changes
0. Run Django locally (see next section), using the debugger if necessary
0. Ensure you have committed all database migration files
0. Create a PR into `staging` from your feature branch
0. (TODO) Check the CI is passing
0. Merge the PR. The branch will be automatically deployed to https://eeasteregg-staging.herokuapp.com/egghunt/
0. Check everything is working on remote
0. Merge changes to `master`
0. Manually deploy changes to https://eeasteregg.herokuapp.com/egghunt/

## Running Locally

0. Make sure you have Python [installed properly](http://install.python-guide.org).  Optionally, install the [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup) for databases. For working with remotes, instal [Heroku Toolbelt](https://toolbelt.heroku.com/)
0. Install Django and the other project requirements
```sh
$ pip install -r requirements.txt
```
0. (Reference) see https://docs.djangoproject.com/en/2.1/intro/tutorial01/ for details of Django.
0. Run
```sh
$ python manage.py migrate
$ python manage.py collectstatic
$ python manage.py runserver
```

Your app should now be running on [127.0.0.1:5000](http://127.0.0.1:5000/).

