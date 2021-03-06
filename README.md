# Dataset manager
A simple tool that aim to help a team manage and export test datasets. It aims to let the dev team define a schema, then
generate a random dataset using this schema and allow people to export it to various target (API, database, elasticsearch, json...)

## TL;DR
````bash
mkdir -p database
docker run --rm -v database:/db -e DATABASE_URL=sqlite:////db/db.sqlite3 -p 8000:8000 exanis/dataset-manager
````

## Warning

I create this tool mainly for my own usage to make some testing easier. While I'll gladly read any request or suggestion,
I can offer no guarantee that it will fit to your needs at all. The easiest way to check is probably to try it...

## Dataset localization

Some data in your dataset may look better if they are localized. You can do that by settings the `LANGUAGE_CODE` environment variable
to whatever you want: fr_FR, it_IT... The default value is en_US. This settings apply to:
- Person field

## Database

Dataset manager is designed to be launched as a docker container (but you can also launch it as a local server). While it
doesn't need *per se* any kind of database (it none are provided, it will use a sqlite one set in ``/tmp/db.sqlite3``),
you will need to recreate your schema and dataset each time you launch the container.

The easiest solution to avoid this is to mount a volume and set the database in it ; this can be done by settings the ``DATABASE_URL``
env variable to a value like this: ``sqlite:////my-great-database-dir/db.sqlite3``. Using this, you will be able to add your
database to your VCS and use it as an asset of your project.

If you have multiple users that keep updating your dataset, another option might be to use a more traditionnal SGBD. You will
need to make sure your docker container (or wherever you're running the tool) have a way to access to it; that may mean
adding a few requirements to python. This is meant to be done by mounting (or editing any way you want) the ``database_requirements.txt``
file. You will then need to update the ``DATABASE_URL`` to point it to your server. An example for a postgres server could be:
``psql://user:mypassword@my-server/my-database``

I test Dataset manager with sqlite3 (and sometime postgres), but there is nothing really strange in it so it should work with any
sgbd supported by Django: postgresql, mysql, sqlite and oracle. However, since I'm using neither mysql nor oracle, I didn't included them to
the requirements file; feel free to send a PR to improve that if needed.

Dataset manager use [django-environ](https://github.com/joke2k/django-environ) to configure database connection. Here is the corresponding url prefix:
- PostgreSQL: ``postgres://``, ``pgsql://``, ``psql://`` or ``postgresql://``
- SQLITE: ``sqlite://``

## Password protection

As I will repeat multiple times in this README, dataset manager is not meant to be publicly accessed. However, you may want to
keep your instance up to avoid launching it on your local computer each time you need it. If you want to do so, you can enable a
password protection (enforced by nginx) by simply setting the ``SERVER_PASSWORD`` environment variable. This variable must be set
to a valid value as could go in a .htpasswd file (since it will basically go in a .htpasswd file), you may do something like:
``-e 'SERVER_PASSWORD=admin:$apr1$2BuSs3Wf$.T9/4Vt1mCOVYE9BdPaBV.'`` (this will set username to admin and the password to admin).

If you need to generate a new password, you can do so by running ``openssl passwd -apr1``.
**Note**: Remember to escape (using ') the argument since the hashed password will include $ char that could be interpreted by your shell

## Other variables

Dataset manager is **not** meant to be publicly accessible. To make it
easier to use, some sensitive stuff (like secret key) are basically ignored. If for some reason you want to make it accessible,
you should really change those settings. The good news is: there are env variable for that! Here is the list of possible variables:

- ``DEBUG``: if set to ``on``, activate Debug mode. Default is ``off``. Should probably stay at off unless you want to work on this project's code
- ``SECRET_KEY``: Django's secret key. Default to ``change me``. There is basically nothing in the project that is signed so it is not that useful; however if you add it (like a password protection), **do not leave it to the default value**. [More about this topic](https://docs.djangoproject.com/en/dev/ref/settings/#secret-key)
- ``ALLOWED_HOSTS``: List of host allowed to be used to access Dataset manager. It default to ``['*']`` (anything), but if you plan on exposing the tool you'd better change it. [More about this topic](https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts)
- ``DATABASE_URL``: See previous section.
- ``LANGUAGE_CODE``: See previous section.
- ``SERVER_PASSWORD``: See previous section.
- ``TIMEZONE``: Allow you to set the timezone used by the application. This is useful for tasks visibility but have no impact on generated data. Default value is UTC.

### Warning

Once again, **be warned that this tools is not meant to be accessed outside of your team**. There is a lot of things that are not enforced
by the code and that are basically never checked after being sent (like, "did the value of this field is of an appropriate type").
This is because it's meant to be used as a tool inside a team that is not likely to go out of it's way and live-edit the HTML to hack itself;
this however is not true when you need to deal with unknown people.

Another potential security issue is that the application, as well as celery, are ran using the **root** user of your docker container.
This is done to avoid potential authorization problem with sqlite databases mounted as volumes, but it may lead to security breach (limited to your docker container, mind you, but still.)

Short version? It's probably a bad idea to make this accessible for everybody. Keep it to your team.

## Accessing the tool

When launched, the tool will listen on port 8000 (please remember to open it - you can use docker port redirection to change it)
