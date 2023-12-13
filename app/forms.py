from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, TextAreaField, DecimalField, IntegerField, SubmitField, HiddenField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
  username = TextAreaField('username', validators=[DataRequired()])
  password = PasswordField('password', validators=[DataRequired()])

class LogoutForm(FlaskForm):
  logout = TextAreaField('username', validators=[DataRequired()])

class RegisterForm(FlaskForm):
  username = TextAreaField('username', validators=[DataRequired()])
  password = PasswordField('password', validators=[DataRequired()])

class AddReviewForm(FlaskForm):
  title = TextAreaField('title', validators=[DataRequired()])
  rating = DecimalField('rating', places=2, validators=[DataRequired()])
  content = TextAreaField('content', validators=[DataRequired()])

class DeleteReviewForm(FlaskForm):
  delete_title = HiddenField('bookId')
  delete_button = SubmitField('Delete')

class AddTransactionForm(FlaskForm):
  name = TextAreaField('name', validators=[DataRequired()])
  amount = DecimalField('amount', places=2, validators=[DataRequired()])
  choices = [('Other','Other'), ('Supermarkets','Supermarkets'), ('Leisure','Leisure'), ('Personal Finance','Personal Finance'), ('Shopping','Shopping'), ('Transport','Transport'), ('Home and Property', 'Home and Property'), ('Personal', 'Personal'), ('Bills', 'Bills'), ('Cash', 'Cash'), ('Cheque', 'Cheque'), ('Gift','Gift'), ('Travel', 'Travel')]
  category = SelectMultipleField('Select the transaction type', choices=choices)
