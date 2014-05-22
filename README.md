# Fakebook

A web site implemented in [bottle](http://bottlepy.org/) and [sqlite3](http://www.sqlite.org/), also using other technology, as needed. For educational purposes, I am not actually trying to get rich.
From here on in Slovene.

## Datoteke

* `bottle.py` -- knjižinica Bottle
* `schema.sql` -- shema za bazo (ukazi `CREATE TABLE`)
* `fakebook.sqlite` -- podatkovna baza
* `fakebook.py` -- strežnik (verzija Python 3)
* `views` -- predloge za spletne strani
* `static` -- statične spletne strani in datoteke


## Namestitev

Najprej naredimo bazo `fakebook.sqlite` z ukazom

    sqlite3 fakebook.sqlite < schema.sql

Nato poženemo strežnik:

    python3 fakebook.py

In to je to.
