"""
Finora – Profit & Loss Analyzer
A simple web application with Google OAuth 2.0 authentication
"""

from flask import Flask, redirect, url_for, session, render_template_string, request
from authlib.integrations.flask_client import OAuth
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Change this to a fixed secret in production

# OAuth Configuration - REPLACE WITH YOUR ACTUAL CREDENTIALS
app.config['GOOGLE_CLIENT_ID'] = 'YOUR_GOOGLE_CLIENT_ID_HERE'
app.config['GOOGLE_CLIENT_SECRET'] = 'YOUR_GOOGLE_CLIENT_SECRET_HERE'

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# HTML Templates as strings
INDEX_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Finora - Profit & Loss Analyzer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            padding: 50px;
            max-width: 500px;
            width: 100%;
            text-align: center;
        }

        .logo {
            font-size: 48px;
            margin-bottom: 20px;
        }

        h1 {
            font-size: 32px;
            color: #333;
            margin-bottom: 10px;
        }

        .tagline {
            color: #666;
            margin-bottom: 40px;
            font-size: 16px;
        }

        .btn-google {
            background: white;
            color: #333;
            border: 2px solid #ddd;
            padding: 12px 30px;
            font-size: 16px;
            border-radius: 50px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            transition: all 0.3s ease;
            text-decoration: none;
        }

        .btn-google:hover {
            border-color: #667eea;
            box-shadow: 0 5px 15px rgba(102,126,234,0.2);
            transform: translateY(-2px);
        }

        .google-icon {
            font-size: 20px;
        }

        .features {
            margin-top: 40px;
            padding-top: 30px;
            border-top: 1px solid #eee;
            display: flex;
            justify-content: center;
            gap: 30px;
            color: #666;
            font-size: 14px;
        }

        .features span {
            display: flex;
            align-items: center;
            gap: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">📊</div>
        <h1>Finora</h1>
        <p class="tagline">Profit & Loss Analyzer</p>
        
        <a href="/login" class="btn-google">
            <span class="google-icon">🔐</span>
            Sign in with Google
        </a>
        
        <div class="features">
            <span>✓ Simple & Fast</span>
            <span>✓ Real-time Analysis</span>
            <span>✓ Secure Login</span>
        </div>
    </div>
</body>
</html>
'''

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Finora</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: #f5f5f5;
        }

        .navbar {
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }

        .logo {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }

        .user-info {
            display: flex;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
        }

        .user-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #667eea;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }

        .user-details {
            text-align: right;
        }

        .user-name {
            font-weight: 600;
            color: #333;
        }

        .user-email {
            font-size: 12px;
            color: #666;
        }

        .logout-btn {
            background: #ff4757;
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            font-size: 14px;
            transition: background 0.3s;
        }

        .logout-btn:hover {
            background: #ff3838;
        }

        .container {
            max-width: 800px;
            margin: 50px auto;
            padding: 0 20px;
        }

        .card {
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        .card h2 {
            color: #333;
            margin-bottom: 30px;
            text-align: center;
        }

        .input-group {
            margin-bottom: 25px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
        }

        input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }

        input:focus {
            outline: none;
            border-color: #667eea;
        }

        .btn-calculate {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 14px;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .btn-calculate:hover {
            transform: translateY(-2px);
        }

        .result {
            margin-top: 30px;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
        }

        .profit {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .loss {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .breakeven {
            background: #fff3cd;
            color: #856404;
            border: 1px solid #ffeeba;
        }

        .profit-value {
            font-size: 36px;
            margin-top: 10px;
        }

        @media (max-width: 600px) {
            .navbar {
                flex-direction: column;
                text-align: center;
            }
            
            .user-info {
                justify-content: center;
            }
            
            .card {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="navbar">
        <div class="logo">Finora 📊</div>
        <div class="user-info">
            <div class="user-details">
                <div class="user-name">{{ user.name }}</div>
                <div class="user-email">{{ user.email }}</div>
            </div>
            <div class="user-avatar">
                {{ user.name[0] }}{{ user.name.split()[-1][0] if ' ' in user.name else '' }}
            </div>
            <a href="/logout" class="logout-btn">Logout</a>
        </div>
    </div>

    <div class="container">
        <div class="card">
            <h2>Profit & Loss Analyzer</h2>
            
            <form method="POST">
                <div class="input-group">
                    <label>💰 Income ($)</label>
                    <input type="number" 
                           name="income" 
                           step="0.01" 
                           placeholder="Enter your total income"
                           value="{{ request.form.get('income', '') }}"
                           required>
                </div>
                
                <div class="input-group">
                    <label>📉 Expenses ($)</label>
                    <input type="number" 
                           name="expenses" 
                           step="0.01" 
                           placeholder="Enter your total expenses"
                           value="{{ request.form.get('expenses', '') }}"
                           required>
                </div>
                
                <button type="submit" class="btn-calculate">Calculate →</button>
            </form>
            
            {% if result %}
            <div class="result {% if 'Profit' in result %}profit{% elif 'Loss' in result %}loss{% elif 'Break-even' in result %}breakeven{% endif %}">
                {% if profit_value > 0 %}
                    🎉 <strong>{{ result }}</strong>
                    <div class="profit-value">+${{ "%.2f"|format(profit_value) }}</div>
                {% elif profit_value < 0 %}
                    😔 <strong>{{ result }}</strong>
                    <div class="profit-value">-${{ "%.2f"|format(profit_value|abs) }}</div>
                {% elif profit_value == 0 and profit_value is not none %}
                    ⚖️ <strong>{{ result }}</strong>
                {% endif %}
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''

LOGOUT_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Logged Out - Finora</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .container {
            background: white;
            border-radius: 20px;
            padding: 50px;
            text-align: center;
            max-width: 400px;
            animation: fadeIn 0.5s ease;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        h2 {
            color: #333;
            margin: 20px 0;
        }

        p {
            color: #666;
            margin-bottom: 30px;
        }

        .btn {
            background: #667eea;
            color: white;
            padding: 12px 30px;
            text-decoration: none;
            border-radius: 5px;
            display: inline-block;
            transition: transform 0.2s;
        }

        .btn:hover {
            transform: translateY(-2px);
        }

        .checkmark {
            font-size: 60px;
            color: #4CAF50;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="checkmark">✓</div>
        <h2>Successfully Logged Out</h2>
        <p>You have been securely logged out of Finora.</p>
        <a href="/" class="btn">Return to Home</a>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template_string(INDEX_TEMPLATE)

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    session['user'] = {
        'name': user_info.get('name'),
        'email': user_info.get('email'),
        'picture': user_info.get('picture')
    }
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    result = None
    profit_value = None
    
    if request.method == 'POST':
        try:
            income = float(request.form.get('income', 0))
            expenses = float(request.form.get('expenses', 0))
            profit_value = income - expenses
            
            if profit_value > 0:
                result = f"Profit: ${profit_value:,.2f}"
            elif profit_value < 0:
                result = f"Loss: ${abs(profit_value):,.2f}"
            else:
                result = "Break-even: $0.00"
        except ValueError:
            result = "Please enter valid numbers"
            profit_value = None
    
    return render_template_string(DASHBOARD_TEMPLATE, 
                                 user=session['user'], 
                                 result=result,
                                 profit_value=profit_value,
                                 request=request)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return render_template_string(LOGOUT_TEMPLATE)

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Finora - Profit & Loss Analyzer")
    print("="*50)
    print("\n📝 Setup Instructions:")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create a new project or select existing")
    print("3. Enable Google+ API and People API")
    print("4. Create OAuth 2.0 Client ID (Web application)")
    print("5. Add redirect URI: http://localhost:5000/authorize")
    print("6. Copy Client ID and Client Secret")
    print("7. Update the credentials in app.py")
    print("\n🔧 Current Configuration:")
    print(f"   Client ID: {app.config['GOOGLE_CLIENT_ID'][:20]}..." if app.config['GOOGLE_CLIENT_ID'] != 'YOUR_GOOGLE_CLIENT_ID_HERE' else "   Client ID: NOT SET")
    print(f"   Client Secret: {'SET' if app.config['GOOGLE_CLIENT_SECRET'] != 'YOUR_GOOGLE_CLIENT_SECRET_HERE' else 'NOT SET'}")
    print("\n" + "="*50)
    print("🌐 Starting server at http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(debug=True, port=5000)