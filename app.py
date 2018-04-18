from flask import Flask, render_template, request, flash, redirect, url_for, g
from flask_login import LoginManager, login_user , logout_user , current_user , login_required
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, PasswordField, BooleanField, validators


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234startrek@localhost/airdropdb'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Dropovi(db.Model):
	__tablename__ = 'dropovi1'
	id = db.Column('id', db.Integer, primary_key=True)
	fulltitle = db.Column('fulltitle', db.String(30))
	shorttitle = db.Column('shorttitle', db.String(4))
	stars = db.Column('stars', db.Integer)
	dollarvalue = db.Column('dollarvalue', db.Integer)
	tokenammount = db.Column('tokenammount', db.Integer)
	reflink = db.Column('reflink', db.String(150))
	active = db.Column('active', db.Boolean)
	telegram = db.Column('telegram', db.Boolean)
	mail = db.Column('mail', db.Boolean)
	twitter = db.Column('twitter', db.Boolean)
	facebook = db.Column('facebook', db.Boolean)
	bitcointalk = db.Column('bitcointalk', db.Boolean)
	reddit = db.Column('reddit', db.Boolean)
	kyc = db.Column('kyc', db.Boolean)
	other = db.Column('other', db.Boolean)

	def __init__(self, id, fulltitle, shorttitle, stars, dollarvalue, tokenammount, reflink, active,
				telegram, mail, twitter, facebook, bitcointalk, reddit, kyc, other):
		self.id = id
		self.fulltitle = fulltitle
		self.shorttitle = shorttitle
		self.stars = stars
		self.dollarvalue = dollarvalue
		self.tokenammount = tokenammount
		self.reflink = reflink
		self.active = active
		self.telegram = telegram
		self.mail = mail
		self.twitter = twitter
		self.facebook = facebook
		self.bitcointalk = bitcointalk
		self.reddit = reddit
		self.kyc = kyc
		self.other = other

class User(db.Model):
	__tablename__ = "users"
	id = db.Column('user_id',db.Integer , primary_key=True)
	username = db.Column('username', db.String(20), unique=True , index=True)
	password = db.Column('password' , db.String(10))
	email = db.Column('email',db.String(50),unique=True , index=True)
	registered_on = db.Column('registered_on' , db.DateTime)

	def __init__(self , username ,password , email):
		self.username = username
		self.password = password
		self.email = email
		self.registered_on = datetime.utcnow()

	def is_authenticated(self):
		 return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.id

	def __repr__(self):
		return '<User %r>' % (self.username)

#All Airdrops
@app.route('/')
def svidropovi():
	svidropovi = Dropovi.query.filter_by(active=True)
	return render_template('index.html', svidropovi=svidropovi)

#FAQ Page
@app.route('/faq')
def faq():
	return render_template('faq.html')

#Admin dashboard 
@app.route('/dashboard')
@login_required
def dashboard():
	svidropovi = Dropovi.query.filter_by(active=True)
	return render_template('dashboard.html', svidropovi=svidropovi)

#User Reguster
@app.route('/register' , methods=['GET','POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html')
	user = User(request.form['username'] , request.form['password'],request.form['email'])
	db.session.add(user)
	db.session.commit()
	flash('User successfully registered')
	return redirect(url_for('login'))

#User Login
@app.route('/login',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	username = request.form['username']
	password = request.form['password']
	registered_user = User.query.filter_by(username=username,password=password).first()
	if registered_user is None:
		flash('Username or Password is invalid' , 'error')
		return redirect(url_for('login'))
	login_user(registered_user)
	flash('Logged in successfully', 'success')
	return redirect(request.args.get('next') or url_for('dashboard'))

#Login manager stuffs
@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))
#More login stuffs
@app.before_request
def before_request():
	g.user = current_user

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('svidropovi')) 
	flash ('Logged out successfully', 'success')

#Form stuffs
class AirdropForm(Form):
	id = StringField('ID')
	fulltitle = StringField('Full Title', [validators.Length(min=1, max=200)])
	shorttitle = StringField('Short Title')
	stars = StringField('Stars')
	dollarvalue = StringField('Dollar Value')
	tokenammount = StringField('Token Amount')
	reflink = StringField('Reflink')
	active = BooleanField('Active')
	telegram = BooleanField('Telegram')
	mail = BooleanField('Mail')
	twitter = BooleanField('Twitter')
	facebook = BooleanField('Facebook')
	bitcointalk = BooleanField('Bitcoin Talk')
	reddit = BooleanField('Reddit')
	kyc = BooleanField('KYC')
	other = BooleanField('Other')

#Add airdrop
@app.route('/add_airdrop', methods=['GET', 'POST'])
@login_required
def add_airdrop():
	form = AirdropForm(request.form)
	if request.method == 'POST' and form.validate():
		#Mislim da je ovo ispod nepotrebno
		id = form.id.data
		fulltitle = form.fulltitle.data
		shorttitle = form.shorttitle.data
		stars = form.stars.data
		dollarvalue = form.dollarvalue.data
		tokenammount = form.tokenammount.data
		reflink = form.reflink.data
		active = form.active.data
		telegram = form.telegram.data
		mail = form.mail.data
		twitter = form.twitter.data
		facebook = form.facebook.data
		bitcointalk = form.bitcointalk.data
		reddit = form.reddit.data
		kyc = form.kyc.data
		other = form.other.data

		# Assign form values to var
		novi1 = Dropovi(id, form.fulltitle.data, form.shorttitle.data, form.stars.data, form.dollarvalue.data, form.tokenammount.data, form.reflink.data, form.active.data, form.telegram.data, form.mail.data, form.twitter.data, form.facebook.data, form.bitcointalk.data, form.reddit.data, form.kyc.data, form.other.data)
		db.session.add(novi1)
		db.session.commit()

		flash('Article Created', 'success')

		return redirect(url_for('dashboard'))

	return render_template('add_airdrop.html', form=form)

@app.route('/edit_airdrop/<string:id>', methods=['POST','GET'])
@login_required
def edit_airdrop(id):
	form= AirdropForm(request.form)
	if request.method == 'POST' and form.validate():

		update_this = Dropovi.query.filter_by(id=id).first()
		update_this.id = form.id.data
		update_this.fulltitle = form.fulltitle.data
		update_this.shorttitle = form.shorttitle.data
		update_this.stars = form.stars.data
		update_this.dollarvalue = form.dollarvalue.data
		update_this.tokenammount = form.tokenammount.data
		update_this.reflink = form.reflink.data
		update_this.active = form.active.data
		update_this.telegram = form.telegram.data
		update_this.mail = form.mail.data
		update_this.twitter = form.twitter.data
		update_this.facebook = form.facebook.data
		update_this.bitcointalk = form.bitcointalk.data
		update_this.reddit = form.reddit.data
		update_this.kyc = form.kyc.data
		update_this.other = form.other.data


		db.session.commit()

		flash('Airdop edited BRAVO OGNJENEE!!!!!!', 'success')

		return redirect(url_for('dashboard'))

	return render_template('edit_airdrop.html', form=form)

#Delete Airdop
@app.route('/delete_airdrop/<string:id>', methods=['POST'])
@login_required
def delete_airdrop(id):
	delete_this = Dropovi.query.filter_by(id=id).first()
	db.session.delete(delete_this)
	db.session.commit()
	flash('Airdrop Deleted', 'success')
	return redirect(url_for('dashboard'))

if __name__ == '__main__':
	app.secret_key='secret123'
	app.run(host='0.0.0.0', debug=True)
