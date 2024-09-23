DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS bookArchive;
DROP TABLE IF EXISTS borrowings;
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  FirstName TEXT NOT NULL,
  LastName TEXT NOT NULL,
  password TEXT NOT NULL,
  DOB TEXT,
  admin INTEGER
);

CREATE TABLE books (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  bookName text UNIQUE NOT NULL,
  author text NOT NULL,
  published TEXT ,
  genre TEXT,
  amount int default 0 check(amount>-1)
);
create table bookArchive(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  bookName text UNIQUE NOT NULL,
  author text NOT NULL,
  published TEXT ,
  genre TEXT
);
create table borrowings(
  id integer primary key AUTOINCREMENT,
  username_id integer,
  book_id integer,
  borrow_date text,
  return_date text
)
