from app import db

class Transaction(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  label = db.Column(db.String(500), index=True)
  group = db.Column(db.Integer) # 0 = Expenditure, 1 = Income
  category = db.Column(db.String(100))
  date = db.Column(db.DateTime)
  amount = db.Column(db.Float)

user_book_assocation = db.Table(
  'user_book_assocation',
  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)

class User(db.Model):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100), index=True, nullable=False)
  password = db.Column(db.String(100), nullable=False)

  books = db.relationship('Book', secondary=user_book_assocation, back_populates='users')
  reviews =  db.relationship('Review', back_populates='user')

class Book(db.Model):
  __tablename__ = 'book'
  id = db.Column(db.Integer, primary_key=True)
  bookId = db.Column(db.String(100), index=True)
  title = db.Column(db.String(500), index=True)
  author = db.Column(db.String(200))
  year_of_publication = db.Column(db.String(100))
  publisher = db.Column(db.String(100))
  imageURL_S = db.Column(db.String(200))
  imageURL_M = db.Column(db.String(200))
  imageURL_L = db.Column(db.String(200))

  users = db.relationship('User', secondary=user_book_assocation, back_populates='books')
  reviews = db.relationship('Review', back_populates='book')

class Review(db.Model):
  __tablename__ = 'review'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
  user = db.relationship("User", back_populates="reviews")
  book = db.relationship("Book", back_populates="reviews")
  content = db.Column(db.String(2000))
  rating = db.Column(db.Integer)

class Like(db.Model):
  __tablename__ = 'like'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
  user = db.relationship("User", backref=db.backref('likes', lazy=True))
  book = db.relationship("Book", backref=db.backref('liked_by', lazy=True))

class Rating(db.Model):
  __tablename__ = 'rating'
  id = db.Column(db.Integer, primary_key=True)
  isbn = db.Column(db.String(100))
  rating = db.Column(db.Integer)


# flask db init
# flask db migrate -m "initial migration"
#   

# p = models.Transaction(label="Dinner", group=0, category="Food/Drink", date=datetime.datetime.utcnow(), amount=25.00)
# u = models.User(username="matty", password="hughes")
# b = models.Book(title="Catch-22", author="Joseph Heller", info="Catch-22 is one of this century's greatest works of American literature. First published m 1961, Joseph Heller's profound and compelling novel has appeared on nearly every list of must read fiction. It is a classic in every sense of the word. Catch-22 took the war novel genre to a new level, shocking us with its clever and disturbing style. Set in a World War II American bomber squadron off the coast of Italy, Catch-22 is the story of John Yossarian, who is furious because thousands of people he has never met are trying to kill him. Yossarian is also trying to decode the meaning of Catch-22, a mysterious regulation that proves that insane people are really the sanest, while the supposedly sensible people are the true madmen. And this novel is full of madmen -- Colonel Cathcart, who keeps raising the number of missions the men must fly m order to finish their tour; Milo Minderbinder, a dedicated entrepreneur who bombs his own airfield when the Germans offer him an extra 6 percent; Major Major Major, whose tragedy in life is that he resembles Henry Fonda; and Major -- de Coverley, whose face is so forbidding no one has dared ask his name. No novel before or since has matched Catch-22's intensity and brilliance in depicting the brutal insanity of war. Heller satirizes military bureaucracy with bitter, stinging humor, all the while telling the darkly comic story of Yossarian, a bombardier who refuses to die. Nearly forty years later, Yossarian lives.")
# r = models.Review(userId=1, bookId=1, content="This is a good book. Thumbs up.", rating=5)

# db.session.add(p)
# db.session.commit()
# models.User.query.get(1)