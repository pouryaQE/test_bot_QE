
from flask import Flask, render_template_string
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ربات تلگرام من</title>
        <style>
            body {
                font-family: 'Tahoma', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                text-align: center;
                max-width: 500px;
            }
            h1 { color: #333; margin-bottom: 20px; }
            .status { 
                background: #4CAF50; 
                color: white; 
                padding: 10px 20px; 
                border-radius: 25px;
                display: inline-block;
                margin: 20px 0;
            }
            .telegram-link {
                background: #0088cc;
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 25px;
                display: inline-block;
                margin-top: 20px;
                transition: background 0.3s;
            }
            .telegram-link:hover { background: #006699; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 ربات تلگرام فعال است!</h1>
            <div class="status">✅ آنلاین</div>
            <p>ربات تلگرام شما با موفقیت در حال اجرا است.</p>
            <p>برای استفاده از ربات، به تلگرام بروید و با ربات چت کنید.</p>
            <a href="https://t.me/YOUR_BOT_USERNAME" class="telegram-link">
                📱 رفتن به ربات
            </a>
        </div>
    </body>
    </html>
    ''')

@app.route('/status')
def status():
    return {'status': 'online', 'message': 'Bot is running successfully!'}

def run_web_server():
    """اجرای وب سرور در thread جداگانه"""
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def start_web_server():
    """شروع وب سرور"""
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    print("🌐 وب سرور روی پورت 5000 شروع شد...")
    return web_thread
