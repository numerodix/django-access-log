django-access-log
=============

Simple traffic analysis

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

How to use
----------

```
./manage.py process_log /path/to/access.log
```
