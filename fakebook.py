#!/usr/bin/env python3

import sqlite3
import bottle
import hashlib # računanje MD5 kriptografski hash (za gesla)

######################################################################
# Konfiguracija

# Datoteka, v kateri je baza
baza_datoteka = "fakebook.sqlite"

# Mapa s statičnimi datotekami
static_dir = "./static"

# Skrivnost za kodiranje cookijev
secret = "to skrivnost je zelo tezko uganiti 1094107c907cw982982c42"


######################################################################
# Pomožne funkcije

def password_md5(s):
    """Vrni MD5 hash danega UTF-8 niza."""
    h = hashlib.md5()
    h.update(s.encode('utf-8'))
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

@bottle.route("/static/<filename:path>")
def static(filename):
    return bottle.static_file(filename, root=static_dir)

@bottle.route("/")
def main():
    (username, ime) = get_user()
    c = baza.cursor()
    c.execute(
    """SELECT ime, datetime(cas,'unixepoch'), vsebina
       FROM trac JOIN uporabnik ON trac.avtor = uporabnik.username
       ORDER BY cas DESC
    """)
    return bottle.template("main.html",
                           ime=ime,
                           username=username,
                           traci=c)

@bottle.get("/login/")
def login_get():
    return bottle.template("login.html",
                           napaka=None,
                           username=None)

@bottle.get("/logout/")
def logout():
    bottle.response.delete_cookie('username')
    bottle.redirect('/login/')

@bottle.post("/login/")
def login_post():
    # Dobimo podatke iz forme
    username = bottle.request.forms.username
    password = bottle.request.forms.password
    # Izračunamo MD5 has gesla, ki ga bomo spravili
    password = password_md5(password)
    # Preverimo, ali se je uporabnik pravilno prijavil
    c = baza.cursor()
    c.execute("SELECT 1 FROM uporabnik WHERE username=? AND password=?",
              [username, password])
    if c.fetchone() is None:
        return bottle.template("login.html",
                               napaka="Nepravilna prijava",
                               username=username)
    else:
        bottle.response.set_cookie('username', username, path='/', secret=secret)
        bottle.redirect("/")

@bottle.get("/register/")
def login_get():
    return bottle.template("register.html", napaka=None)

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
        # Uporabnik že obstaja
        return bottle.template("register.html",
                               napaka='To uporabniško ime je že zavzeto')
    elif not password1 == password2:
        # Geslo se ne ujemata
        return bottle.template("register.html",
                               napaka='Gesli se ne ujemata')
    else:
        # Vse je v redu, vstavi novega uporabnika v bazo
        password = password_md5(password1)
        c.execute("INSERT INTO uporabnik (username, ime, password) VALUES (?, ?, ?)",
                  (username, ime, password))
        # Daj uporabniku cookie
        bottle.response.set_cookie('username', username, path='/', secret=secret)
        bottle.redirect("/")

@bottle.post("/new-trac/")
def new_trac():
    (username, ime) = get_user()
    trac = bottle.request.forms.trac
    c = baza.cursor()
    c.execute("INSERT INTO trac (avtor, vsebina) VALUES (?,?)",
              [username, trac])
    return bottle.redirect("/")
        
@bottle.route("/user/<username>/")
def user_page(username):
    c = baza.cursor()
    # Ime tega uporabnika (hkrati preverimo, ali uporabnik sploh obstaja)
    c.execute("SELECT ime FROM uporabnik WHERE username=?", [username])
    (ime,) = c.fetchone()
    # Prikaži vse trače tega uporabnika
    c.execute(
    """SELECT ime, datetime(cas,'unixepoch'), vsebina
       FROM trac JOIN uporabnik ON trac.avtor = uporabnik.username
       WHERE avtor=? ORDER BY cas DESC
    """,
        [username])
    return bottle.template("user.html",
                           ime=ime,
                           username=username,
                           traci=c)


######################################################################
# Glavni program

# priklopimo se na bazo
baza = sqlite3.connect(baza_datoteka, isolation_level=None)

# poženemo strežnik na portu 8080, glej http://localhost:8080/
bottle.run(host='localhost', port=8080, reloader=True)
