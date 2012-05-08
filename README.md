django-access-log
=============

Simple traffic analysis. Parse access.log, inspect your traffic in the admin, discover common/recent error pages.

Requirements
------------

python-dateutil

Install
-------

    $ pip install -e git://github.com/numerodix/django-access-log.git#egg=django-access-log

Then add:

```python
INSTALLED_APPS = (
    ..
    'access_log',
    ..
)
```

Then initialize the database tables:

```
./manage.py migrate access_log
```


How to use
----------

```
./manage.py process_log /path/to/access.log
```

Then see the Access_Log app in the admin.
