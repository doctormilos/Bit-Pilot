import os
from flask import Flask, render_template, request, flash, redirect, url_for, g
from flask_login import LoginManager, login_user , logout_user , current_user , login_required
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, TextAreaField, PasswordField, BooleanField, validators
from flask_wtf import Form
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234startrek@localhost/airdropdb'
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
	tutorijala = db.Column('tutorijala', db.String(500))
	tutorijalb = db.Column('tutorijalb', db.String(500))
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

	def __init__(self, id, fulltitle, shorttitle, stars, tutorijala, tutorijalb, dollarvalue, tokenammount, reflink, active,
				telegram, mail, twitter, facebook, bitcointalk, reddit, kyc, other):
		self.id = id
		self.fulltitle = fulltitle
		self.shorttitle = shorttitle
		self.stars = stars
		self.tutorijala = tutorijala
		self.tutorijalb = tutorijalb
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

class Fauceti(db.Model):
	__tablename__ = 'fauceti'
	id = db.Column('id', db.Integer, primary_key=True)
	title = db.Column('title', db.String(30))
	stars = db.Column('stars', db.Integer)
	info = db.Column('info', db.String(500))
	vrednost = db.Column('vrednost', db.String(50))
	reflink = db.Column('reflink', db.String(150))
	limit = db.Column('limit', db.String(30))
	period = db.Column('period', db.String(30))
	active = db.Column('active', db.Boolean)
	coin = db.Column('coin', db.String(30))


	def __init__(self, id, title, stars, info, vrednost, reflink, limit, period, active, coin):
		self.id = id
		self.title = title
		self.stars = stars
		self.info = info
		self.vrednost = vrednost
		self.reflink = reflink
		self.limit = limit
		self.period = period
		self.active = active
		self.coin = coin

#All Airdrops
@app.route('/pocetna')
def svidropovisrb():
	svidropovi = Dropovi.query.filter_by(active=True)
	return render_template('pocetna.html', svidropovi=svidropovi)

#All Airdrops
@app.route('/')
def svidropovi():
	svidropovi = Dropovi.query.filter_by(active=True)
	return render_template('index.html', svidropovi=svidropovi)

#All Faucets
@app.route('/faucets')
def svifauceti():
	svifauceti = Fauceti.query.filter_by(active=True)
	return render_template('faucets.html', svifauceti=svifauceti)

#FAQ Page
@app.route('/faq')
def faq():
	return render_template('faq.html')

#CPP stranica
@app.route('/cpp')
def cpp():
	return render_template('cesto-postavljana-pitanja.html')

#Kako-da page
@app.route('/kako-da')
def kako():
	return render_template('kako-da.html')

#How-to page
@app.route('/how-to')
def howto():
	return render_template('howto.html')

#Admin dashboard 
@app.route('/dashboard')
@login_required
def dashboard():
	svidropovi = Dropovi.query.filter_by(active=True)
	return render_template('dashboard.html', svidropovi=svidropovi)

#User Register
@app.route('/register' , methods=['GET','POST'])
@login_required
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

#Airdrop form stuffs
class AirdropForm(Form):
	photo = FileField()
	id = StringField('ID')
	fulltitle = StringField('Full Title', [validators.Length(min=1, max=200)])
	shorttitle = StringField('Short Title')
	stars = StringField('Stars')
	tutorijala = TextAreaField('Tutorijal Engleski')
	tutorijalb = TextAreaField('Tutorijal Srpski')
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


#Faucet form stuffs
class FaucetForm(Form):
	id = StringField('ID')
	title = StringField('Title', [validators.Length(min=1, max=200)])
	stars = StringField('Stars')
	info = TextAreaField('Info')
	vrednost = TextAreaField('Vrednost po danu')
	reflink = StringField('Reflink')
	limit = StringField('Limit za podizanje')
	period = StringField('Period')
	active = BooleanField('Aktivan')
	coin = StringField('Koji coin')

#Add picture

class UploadForm(Form):
	photo = FileField()

@app.route('/add_picture', methods=['GET', 'POST'])
@login_required
def add_picture():
	
	form = UploadForm()
	hists = os.listdir('static/drops')
	hists = ['drops/' + file for file in hists if file.lower().endswith(".png")]
	
	if form.validate_on_submit():
		filename = secure_filename(form.photo.data.filename)
		form.photo.data.save('static/drops/' + filename)

		flash('bravo', 'success')
		return redirect(url_for('dashboard'))

	return render_template('add_picture.html', form=form, hists=hists)

#Add airdrop
@app.route('/add_airdrop', methods=['GET', 'POST'])
@login_required
def add_airdrop():
	form = AirdropForm(request.form)
	if request.method == 'POST':
		#	TEND TO THIS 		
		#		 |
		# Ne radi form.validate() iz nekog razloga
		#
		# Call init self for form data
		novi2 = Dropovi(form.id.data, form.fulltitle.data, form.shorttitle.data, form.stars.data, form.tutorijala.data, form.tutorijalb.data, form.dollarvalue.data, form.tokenammount.data, form.reflink.data, form.active.data, form.telegram.data, form.mail.data, form.twitter.data, form.facebook.data, form.bitcointalk.data, form.reddit.data, form.kyc.data, form.other.data)
		db.session.add(novi2)
		db.session.commit()

		flash('Article Created', 'success')

		return redirect(url_for('dashboard'))

	return render_template('add_airdrop.html', form=form)

@app.route('/add_faucet', methods=['GET', 'POST'])
@login_required
def add_faucet():
	form = FaucetForm(request.form)
	if request.method == 'POST':
		#	TEND TO THIS 		
		#		 |
		# Ne radi form.validate() iz nekog razloga
		#
		# Call init self for form data
		novi2 = Fauceti(form.id.data, form.fulltitle.data, form.shorttitle.data, form.stars.data, form.tutorijala.data, form.tutorijalb.data, form.dollarvalue.data, form.tokenammount.data, form.reflink.data, form.active.data, form.telegram.data, form.mail.data, form.twitter.data, form.facebook.data, form.bitcointalk.data, form.reddit.data, form.kyc.data, form.other.data)
		db.session.add(novi2)
		db.session.commit()

		flash('Faucet Created', 'success')

		return redirect(url_for('dashboard'))

	return render_template('add_faucet.html', form=form)

@app.route('/edit_airdrop/<string:id>', methods=['POST','GET'])
@login_required
def edit_airdrop(id):
	form= AirdropForm(request.form)
	info = Dropovi.query.filter_by(id=id).first()
	
	if request.method == 'POST':

		update_this = Dropovi.query.filter_by(id=id).first()
		update_this.id = form.id.data
		update_this.fulltitle = form.fulltitle.data
		update_this.shorttitle = form.shorttitle.data
		update_this.stars = form.stars.data
		update_this.tutorijala = form.tutorijala.data
		update_this.tutorijalb = form.tutorijalb.data
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

		flash('Airdop edited :)', 'success')

		return redirect(url_for('dashboard'))

	return render_template('edit_airdrop.html', form=form, info=info)

#Delete Airdop
@app.route('/delete_airdrop/<string:id>', methods=['POST'])
@login_required
def delete_airdrop(id):
	delete_this = Dropovi.query.filter_by(id=id).first()
	db.session.delete(delete_this)
	db.session.commit()
	flash('Airdrop Deleted', 'success')
	return redirect(url_for('dashboard'))

#Delete picture - moram da secem string - na template radi replace funkciju jinja2
@app.route('/delete_picture/<string:id>', methods=['POST'])
@login_required
def delete_picture(id):
	os.remove('static/drops/' + id)
	flash('Picture Deleted', 'success')
	return redirect(url_for('dashboard'))

if __name__ == '__main__':
	app.secret_key='secret123'
	app.run(host='0.0.0.0', debug=True)
