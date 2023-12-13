from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import csv
from app import db, models

with open('books.csv', 'r') as csvfile:
  csv_reader = csv.reader(csvfile)
  next(csv_reader)
  id = 0
  for row in csv_reader:
    if len(row) >= 8:
      id+=1
      bookId, title, author, year, publisher, imageS, imageM, imageL= row[:8]
      record = models.Book(id=id, bookId=bookId, title=title, author=author, year_of_publication=year, publisher=publisher, imageURL_S=imageS, imageURL_M=imageM, imageURL_L=imageL)
      db.session.add(record)
      db.session.commit()

with open('ratings.csv', 'r') as csvfile2:
  csv_reader = csv.reader(csvfile2)
  next(csv_reader)
  id = 0
  for row in csv_reader:
    if len(row) >= 3:
      id+=1
      userId, isbn, rating = row[:3]
      record = models.Rating(id=id, isbn=isbn, rating=int(rating))
      db.session.add(record)
      db.session.commit()
