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

def geslo_md5(s):
    """Vrni MD5 hash danega UTF-8 niza."""
    h = hashlib.md5()
    h.update(s.encode('utf-8'))
    return h.hexdigest()

######################################################################
# Server

@bottle.route("/")
def main():
    email = bottle.request.get_cookie('email', secret=secret)
    if email is None:
        bottle.redirect("/login/")
    else:
        c = baza.cursor()
        c.execute("SELECT ime FROM uporabnik WHERE email=?",
                  [email])
        (ime,) = c.fetchone()
        return bottle.template("main.html", ime=ime)

@bottle.get("/login/")
def login_get():
    return bottle.template("login.html",
                           napaka=None,
                           email="")

@bottle.post("/login/")
def login_post():
    email = bottle.request.forms.get('email')
    geslo = bottle.request.forms.get('geslo')
    print ("email = {0}, geslo = {1}".format(email, geslo_md5(geslo)))
    c = baza.cursor()
    c.execute("SELECT 1 FROM uporabnik WHERE email=? AND geslo=?",
              [email, geslo_md5(geslo)])
    if c.fetchone() is None:
        return bottle.template("login.html",
                               napaka="Napačno uporabniško ime ali geslo",
                               email=email)
    else:
        bottle.response.set_cookie('email', email, path='/', secret=secret)
        bottle.redirect("/")


@bottle.get("/register/")
def login_get():
    return bottle.template("register.html")

@bottle.post("/register/")
def register_post():
    email = bottle.request.forms.get('email')
    ime = bottle.request.forms.get('ime')
    geslo1 = bottle.request.forms.get('geslo1')
    geslo2 = bottle.request.forms.get('geslo2')
    # Ali uporabnik že obstaja
    c = baza.cursor()
    c.execute("SELECT 1 FROM uporabnik WHERE email=?", [email])
    if c.fetchone():
        return "Ste se ze registrirali"
    elif not geslo1 == geslo2:
        return "Gesli se ne ujemata"
    else:
        geslo = geslo_md5(geslo1)
        c.execute("INSERT INTO uporabnik (email, ime, geslo) VALUES (?, ?, ?)",
                  (email, ime, geslo))
        return "Ste registrirani."

######################################################################
# Glavni program

# priklopimo se na bazo
baza = sqlite3.connect(baza_datoteka, isolation_level=None)

# poženemo strežnik na portu 8080, glej http://localhost:8080/
bottle.run(host='localhost', port=8080, reloader=True)
