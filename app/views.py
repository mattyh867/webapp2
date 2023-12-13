from flask import render_template, request, Flask, redirect, url_for, session, jsonify
from app import app, db, admin, models
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from .forms import LoginForm, AddReviewForm, RegisterForm
from flask_bcrypt import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
import random
import json

# Set the starting webpage to the homepage
@app.route('/', methods=['POST', 'GET'])
def index():
  if 'user_id' in session:
    return redirect(url_for('homepage'))
  else:
    return redirect(url_for('login'))
  
@app.route('/login', methods=['GET', 'POST'])
def login():
  if 'user_id' in session:
    session.pop('user_id', None)

  session['data'] = ['', 0, '']

  form = LoginForm()
  if form.validate_on_submit():
    user = models.User.query.filter_by(username=form.username.data).first()

    if user and check_password_hash(user.password, form.password.data):
      session['user_id'] = form.username.data
      return redirect(url_for('homepage'))
    else:
      return redirect(url_for('login'))
  
  return render_template('login.html',
                         title='Log In',
                         form=form,
                         )

@app.route('/logout')
def logout():
  session.pop('user_id', None)
  return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegisterForm()

  if form.validate_on_submit():
    username = form.username.data
    password = generate_password_hash(form.password.data)

    user_exists = models.User.query.filter_by(username=username).first()

    if not user_exists:
      new_user = models.User(username=username, password=password)
      db.session.add(new_user)
      db.session.commit()
      return redirect(url_for('homepage'))
    else:
      return redirect(url_for('register'))
  
  return render_template('register.html',
                         title='Register',
                         form=form,
                         )

@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
  if 'user_id' not in session:
    return redirect(url_for('login'))
  
  sessionUser = session['user_id']
  
  p = models.Book.query.get(random.randint(1,174040))
  spotlightTitle = p.title
  spotlightAuthor = p.author
  spotlightImg = p.imageURL_L

  ratings = models.Rating.query.filter_by(isbn=p.bookId).all()
  ratingCount = len(ratings)
  
  # calculating the average rating of the spotlight book
  totalRating = 0
  for i in ratings:
    totalRating += i.rating

  if ratingCount != 0:
    averageRating = round((totalRating / ratingCount), 2)
  else:
    averageRating = 'Rating unavailable'

  bookId = p.bookId

  return render_template('homepage.html',
                         title='Homepage',
                         spotlightTitle=spotlightTitle,
                         spotlightAuthor=spotlightAuthor,
                         spotlightImg=spotlightImg,
                         averageRating=averageRating,
                         sessionUser=sessionUser,
                         bookId=bookId,
                         )

@app.route('/your_reviews', methods=['GET', 'POST'])
def your_reviews():
  if 'user_id' not in session:
      return redirect(url_for('login'))
  
  sessionUser = session['user_id']
  user = models.User.query.filter_by(username=sessionUser).first()

  data = session['data']
  if data is None:
    data = ['', 0, '']

  default_data = {
    'title': data[0],
    'rating': data[1],
    'content': data[2],
  }

  reviews = models.Review.query.filter_by(user_id=user.id).all()
  reviewBook = []
  reviewRating = []
  reviewContent = []
  reviewImg = []
  reviewId = []
  reviewBookId = []
  reviewCount = 0
  
  for r in reviews:
    reviewId.append(r.id)
    validatedId = "{:0>10}".format(r.book_id)
    reviewBookId.append(validatedId)
    bookTitle = models.Book.query.filter_by(bookId=validatedId).first().title
    bookImg = models.Book.query.filter_by(bookId=validatedId).first().imageURL_S
    reviewBook.append(bookTitle)
    reviewRating.append(r.rating)
    reviewContent.append(r.content)
    reviewImg.append(bookImg)
    reviewCount += 1
    # reviewBook.append(validatedId)

  form = AddReviewForm(data=default_data)

  if form.validate_on_submit():
    bookExists = models.Book.query.filter_by(title=form.title.data).first()

    if bookExists:
      newReview = models.Review(user_id=user.id, book_id=bookExists.bookId, content=form.content.data, rating=int(form.rating.data))
      db.session.add(newReview)
      db.session.commit()
      return redirect(url_for('your_reviews'))
    else:
      newData = [form.title.data, form.rating.data, form.content.data]
      session['data'] = newData
      return  redirect(url_for('your_reviews'))

  return render_template('your_reviews.html',
                         title='Your Reviews',
                         reviewBook=reviewBook,
                         reviewRating=reviewRating,
                         reviewContent=reviewContent,
                         reviewCount=reviewCount,
                         reviewImg=reviewImg,
                         reviewId=reviewId,
                         reviewBookId=reviewBookId,
                         form=form,
                         data=data,       
                         sessionUser=sessionUser,
                         )

@app.route('/your_likes', methods=['GET', 'POST'])
def your_likes():
  if 'user_id' not in session:
      return redirect(url_for('login'))
  
  sessionUser = session['user_id']

  user = models.User.query.filter_by(username=sessionUser).first()

  likes = models.Like.query.filter_by(user_id=user.id).all()
  likeBook = []
  likeAuthor = []
  likeImg = []
  likeId = []
  likeBookId = []
  likeCount = 0
  
  for l in likes:
    likeId.append(l.id)
    validatedId = "{:0>10}".format(l.book_id)
    likeBookId.append(validatedId)
    bookTitle = models.Book.query.filter_by(bookId=validatedId).first().title
    bookAuthor = models.Book.query.filter_by(bookId=validatedId).first().author
    bookImg = models.Book.query.filter_by(bookId=validatedId).first().imageURL_S
    likeAuthor.append(bookAuthor)
    likeBook.append(bookTitle)
    likeImg.append(bookImg)
    likeCount += 1
    # likeBook.append(l.book_id)

  return render_template('your_likes.html',
                         title='Your Likes',
                         likeBook=likeBook,
                         likeAuthor=likeAuthor,
                         likeCount=likeCount,
                         likeImg=likeImg,
                         likeId=likeId,
                         likeBookId=likeBookId, 
                         sessionUser=sessionUser,
                         )

# Endpoint for when the delete button of a review is clicked
@app.route('/delete_review', methods=['POST'])
def delete_review():
  if 'user_id' not in session:
    return redirect(url_for('login'))
  
  record = request.form.get('review_id')

  if record is None:
    return redirect(url_for('your_reviews'))
  
  p = models.Review.query.get(record)
  db.session.delete(p)
  db.session.commit()
  return redirect(url_for('your_reviews'))
  
# Endpoint for when the like of a book is deleted
@app.route('/delete_like', methods=['POST'])
def delete_like():
  if 'user_id' not in session:
    return redirect(url_for('login'))
  
  record = request.form.get('like_id')

  if record is None:
    return redirect(url_for('your_likes'))
  
  p = models.Like.query.get(record)
  db.session.delete(p)
  db.session.commit()
  return redirect(url_for('your_likes'))

# Route for the like button
@app.route('/like', methods=['POST'])
def like():
  if 'user_id' not in session:
    return redirect(url_for('login'))
  
  username = session['user_id']
  user = models.User.query.filter_by(username=username).first()
  
  # Process response

  book_id = request.form.get('book_id')

  # Check if like exists
  existing_like = models.Like.query.filter_by(user_id=user.id, book_id=book_id).first()

  if existing_like:
    return jsonify({'message': 'liked', 'status': 'error'})
  
  new_like = models.Like(user_id=user.id, book_id=book_id)

  db.session.add(new_like)
  db.session.commit()

  # Return request to javascript
  # return json.dumps({'status': 'OK', 'response': response})
  return jsonify({'message': 'SUCCESS', 'status': 'success'})