from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import csv
from app import db, models

with open('ratings.csv', 'r') as csvfile:
  csv_reader = csv.reader(csvfile)
  next(csv_reader)
  id = 0
  for row in csv_reader:
    s = models.Rating.query.filter_by(id=id).first()
    if s is None:
      if len(row) >= 3:
        id+=1
        userId, isbn, rating = row[:3]

        book = models.Book.query.filter_by(bookId=isbn).first()

        if book:
          record = models.Rating(isbn=isbn, rating=int(rating))
          db.session.add(record)
          db.session.commit()
