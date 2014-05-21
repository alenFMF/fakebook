-- Shema za Fakebook bazo

CREATE TABLE IF NOT EXISTS uporabnik (
  email TEXT PRIMARY KEY,
  ime TEXT NOT NULL,
  geslo TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS trac (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  avtor TEXT NOT NULL REFERENCES uporabnik (email),
  cas INTEGER NOT NULL,
  vsebina TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS komentar (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  vsebina TEXT NOT NULL,
  trac INTEGER NOT NULL REFERENCES trac (id),
  avtor TEXT NOT NULL REFERENCES uporabnik (email),
  cas INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS frend (
  uporabnik TEXT NOT NULL REFERENCES uporabnik (email),
  frend TEXT NOT NULL REFERENCES uporabnik (email),
  CONSTRAINT frend_key PRIMARY KEY (uporabnik, frend)
);
