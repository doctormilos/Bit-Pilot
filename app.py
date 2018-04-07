from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234startrek@localhost/airdropdb'
db = SQLAlchemy(app)

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


#Single Airdrop
@app.route('/airdrop/<string:id>/')
def airdop(id):
	airdrop = Dropovi.query.filter_by(id=id).first()
	return render_template('index.html', airdrop=airdrop)


if __name__ == '__main__':
	app.secret_key='secret123'
	app.run(debug=True)
