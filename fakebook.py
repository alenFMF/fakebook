#!/usr/bin/env python3

import sqlite3
import bottle
import hashlib

######################################################################
# Konfiguracija

# Datoteka, v kateri je baza
baza_datoteka = "fakebook.sqlite"

# Skrivnost za kodiranje cookijev
#secret = "acbd18db4cc2f85cedef654fccc4a4d8"
secret=None

######################################################################
# Pomožne funkcije

def password_md5(s):
    """Vrni MD5 hash danega UTF-8 niza."""
    h = hashlib.md5()
    h.update(s)
    return h.hexdigest()

def get_user():
    username = bottle.request.get_cookie('username', secret=secret)
    if username is not None:
        c = baza.cursor()
        c.execute("SELECT username, ime FROM uporabnik WHERE username=?",
                  [username])
        r = c.fetchone()
        if r is not None: return r
    bottle.redirect('/login/')

######################################################################
# Server

@bottle.route("/")
def main():
    (username, ime) = get_user()
    c = baza.cursor()
    c.execute(
    """SELECT ime, datetime(cas,'unixepoch'), vsebina
       FROM trac JOIN uporabnik ON trac.avtor = uporabnik.username
       WHERE avtor=? ORDER BY cas DESC
    """,
        [username])
    return bottle.template("main.html",
                           ime=ime,
                           username=username,
                           traci=c)

@bottle.get("/login/")
def login_get():
    return bottle.template("login.html",
                           napaka=None,
                           username="")

@bottle.post("/login/")
def login_post():
    username = bottle.request.forms.username
    password = bottle.request.forms.password
    password = password_md5(password)
    print ("username = {0}, password = {1}".format(username, password))
    c = baza.cursor()
    c.execute("SELECT 1 FROM uporabnik WHERE username=? AND password=?",
              [username, password])
    if c.fetchone() is None:
        return bottle.template("login.html",
                               napaka="Napačno uporabniško ime ali password",
                               username=username)
    else:
        bottle.response.set_cookie('username', username, path='/', secret=secret)
        bottle.redirect("/")

@bottle.get("/register/")
def login_get():
    return bottle.template("register.html")

@bottle.post("/register/")
def register_post():
    username = bottle.request.forms.username
    ime = bottle.request.forms.ime
    password1 = bottle.request.forms.password1
    password2 = bottle.request.forms.password2
    # Ali uporabnik že obstaja
    c = baza.cursor()
    c.execute("SELECT 1 FROM uporabnik WHERE username=?", [username])
    if c.fetchone():
        return "Ste se ze registrirali"
    elif not password1 == password2:
        return "Gesli se ne ujemata"
    else:
        password = password_md5(password1)
        c.execute("INSERT INTO uporabnik (username, ime, password) VALUES (?, ?, ?)",
                  (username, ime, password))
        return "Ste registrirani."

@bottle.post("/new-trac/")
def new_trac():
    (username, ime) = get_user()
    trac = bottle.request.forms.trac
    c = baza.cursor()
    c.execute("INSERT INTO trac (avtor, vsebina) VALUES (?,?)",
              [username, trac])
    return bottle.redirect("/")
        


######################################################################
# Glavni program

# priklopimo se na bazo
baza = sqlite3.connect(baza_datoteka, isolation_level=None)

# poženemo strežnik na portu 8080, glej http://localhost:8080/
bottle.run(host='localhost', port=8080, reloader=True)
