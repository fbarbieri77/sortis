__author__ = "Fabio Barbieri"

from flask import Flask, render_template, request, session, make_response
from src.common.database import Database
from src.models.user import User
from src.models.dashboard import Dashboard
from src.models.bet import Bet


from src.models.security import Security

app = Flask(__name__) # '__main__', running the app directly
app.secret_key = "guilherme"

@app.route('/') # defines an empty end point
@app.route('/<string:message>')
def home_temmplate(message=None):
    if 'email' not in session or session['email'] == None:
        return render_template('login.html', message=message)
    else:
        return render_template('base.html')

@app.route('/login/<string:message>') # defines an empty end point
def login_temmplate(message):
    return render_template('login.html', message=message)

@app.route('/register') # defines an empty end point
def register_template():
    return render_template('register.html')

@app.before_first_request
def initialize_database():
    Database.initialize("sortis")

@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    
    if User.login_valid(email, password):
        User.login(email)
        message=None
    else:
        session['email'] = None
        message='Usuário inválido!'

    return make_response(home_temmplate(message))

@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)

    return render_template('dashboard.html', email=session['email'])
    
@app.route('/dashboard/<string:user_id>')
@app.route('/dashboard')
def start_dashboard(user_id=None):
    if user_id is not None:
        user_dashboard = Dashboard(user_id)
    elif 'email' in session and session['email'] is not None:
        user = User.get_by_email(session['email'])
        user_dashboard = Dashboard(user._id)
    else:
        return make_response(login_temmplate('Usuário inválido!'))

    basket = user_dashboard.get_bets()

    return render_template('dashboard.html', bets=basket)

@app.route('/assets')
def available_assets():
    if 'email' in session and session['email'] is not None:
        assets = Security.get_all()    
        return render_template('assets.html', bets=assets)
    else:
        return make_response(home_temmplate('Usuário inválido!'))

@app.route('/security/<string:asset_id>&<string:page>')
def bet_details(asset_id, page):
    security = Security.from_mongo(asset_id)
    return render_template('buy.html', asset=security, origin=page)


@app.route('/check-security/<string:security_id>&<string:page>')
def check_security(security_id, page):
    asset = Security.from_mongo(security_id)
    
    return render_template('check-security.html', bet=asset, origin=page)

@app.route('/buy/<string:security_id>')
def buy_asset(security_id, user_id=None):
    if user_id is None:
        user = User.get_by_email(session['email'])
        user_id = user._id

    new_bet = Bet(user_id, security_id)
    new_bet.save_to_mongo()

    return make_response(start_dashboard(user_id))

@app.route('/scratch/<string:asset_id>&<string:title>')
def scratch(asset_id, title):
    security = Security.from_mongo(asset_id)

    list = security.prizes
    i=0
    for prizes in list:
        if prizes['title'] == title:
            security.prizes[i]['is_checked'] = True
            break
        i += 1 

    security.update_mongo()

    return make_response(check_security(asset_id, 'dashboard'))

@app.route('/logout')
def logout():
    session['email'] = None
    return render_template('login.html', message=None)

@app.route('/security')
def new_security():
    return render_template('add-security.html')

@app.route('/add-security', methods=['POST'])
def add_security():
    author = request.form['author']
    value = float(request.form['value'])
    
    title_1 = request.form['title_1']
    is_winner_1 = request.form['is_winner_1']
    title_2 = request.form['title_2']
    is_winner_2 = request.form['is_winner_2']
    title_3 = request.form['title_3']
    is_winner_3 = request.form['is_winner_3']
    title_4 = request.form['title_4']
    is_winner_4 = request.form['is_winner_4']

    prizes = []
    if len(title_1) > 0:
        prizes.append(
        {
            'title': title_1,
            'is_winner': False if is_winner_1=='false' else True,
            'is_checked': False
        })
    if len(title_2) > 0:
        prizes.append(
        {
            'title': title_2,
            'is_winner': False if is_winner_2=='false' else True,
            'is_checked': False
        })
    if len(title_3) > 0:
        prizes.append(
        {
            'title': title_3,
            'is_winner': False if is_winner_3=='false' else True,
            'is_checked': False
        })
    if len(title_4) > 0:
        prizes.append(
        {
            'title': title_4,
            'is_winner': False if is_winner_4=='false' else True,
            'is_checked': False
        })

    security = Security(author, value, prizes)
    security.save_to_mongo()

    return render_template('add-security.html')


if __name__ == '__main__':
    """
    Database.initialize("sortis")
    assets = [
        {
        "author": "Seg Cap",
        "value": 40,
        "prizes": [{"title": "Casa", "is_winner": False}, 
                    {"title": "Carro", "is_winner": False}, 
                    {"title": "Mercado", "is_winner": False}],
        "is_winner": False
        },
        {
        "author": "Seg Cap",
        "value": 40,
        "prizes": [{"title": "Casa", "is_winner": False}, 
                    {"title": "Carro", "is_winner": True}, 
                    {"title": "Mercado", "is_winner": False}],
        "is_winner": False
        },
        {
        "author": "Seg Cap",
        "value": 40,
        "prizes": [{"title": "Casa", "is_winner": True}, 
                    {"title": "Carro", "is_winner": False}, 
                    {"title": "Mercado", "is_winner": False}],
        "is_winner": True
        }
    ]

    for asset in assets:
        #ecurity_id, author, value, prizes, is_winner=False, is_checked=False, _id=None
        security = Security(author=asset["author"], value=asset["value"], prizes=asset["prizes"], is_winner=asset["is_winner"])
        security.save_to_mongo()
    """
    app.run()
