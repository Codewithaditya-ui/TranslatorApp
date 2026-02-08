import os
import threading
import time
from pywebio.input import textarea, select
from pywebio.output import put_text, put_html, clear, use_scope
from deep_translator import GoogleTranslator
from pywebio.platform.flask import webio_view
from flask import Flask

# 1. Initialize the Background Server
app = Flask(__name__)

def translator_logic():
    # CSS for Bold Text, Animations, and 3-Layer Background
    put_html("""
    <style>
        body {
            background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            min-height: 100vh;
            color: white;
            font-family: 'Arial Black', Gadget, sans-serif;
        }
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .main-card {
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(15px);
            border-radius: 30px;
            padding: 40px;
            margin: 20px auto;
            max-width: 650px;
            border: 2px solid rgba(255, 255, 255, 0.4);
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        }
        h1 { font-weight: 900; color: #ffffff; font-size: 2.5em; text-align: center; text-shadow: 2px 2px 4px #000; }
        .result-box {
            background: #ffffff;
            color: #333;
            padding: 20px;
            border-radius: 15px;
            margin-top: 25px;
            font-weight: 900;
            font-size: 1.3em;
            border-left: 10px solid #fdbb2d;
        }
    </style>
    """)

    put_html("<div class='main-card'>")
    put_html("<h1>✨ ADITYA'S PRO APP</h1>")
    
    while True:
        text = textarea("ENTER TEXT", placeholder="Type your message here...")
        
        # Comprehensive Language List
        langs = {
            'HINDI': 'hindi', 'BENGALI': 'bengali', 'ODIA': 'odia', 
            'PUNJABI': 'punjabi', 'ENGLISH': 'english', 'FRENCH': 'french',
            'GERMAN': 'german', 'SPANISH': 'spanish'
        }
        
        target = select("SELECT TARGET LANGUAGE", list(langs.keys()))
        
        with use_scope('res', clear=True):
            put_text("Translating... ⏳")
            try:
                translated = GoogleTranslator(source='auto', target=langs[target]).translate(text)
                clear('res')
                put_html(f"""
                <div class='result-box'>
                    <span style='color: #888; font-size: 0.8em;'>ORIGINAL:</span><br>{text}<hr>
                    <span style='color: #b21f1f;'>{target}:</span><br>{translated}
                </div>
                """)
            except Exception as e:
                clear('res')
                put_text(f"Connection Error: Check your Internet!")

# Integration for Render/Web
app.add_url_rule('/', 'webio_view', webio_view(translator_logic), methods=['GET', 'POST', 'OPTIONS'])

if __name__ == '__main__':
    # Determine if we are on Render (Web) or local Mac
    is_on_render = os.environ.get("RENDER", None)
    port = int(os.environ.get("PORT", 5000))

    if is_on_render:
        # WEB MODE: Just run the server for Render
        app.run(host='0.0.0.0', port=port)
    else:
        # MAC APP MODE: Run in background and open a window
        import webview
        
        def run_server():
            app.run(port=port, debug=False, threaded=True)

        t = threading.Thread(target=run_server)
        t.daemon = True
        t.start()
        
        time.sleep(2)
        webview.create_window("Aditya's Ultimate Translator", f"http://127.0.0.1:{port}", width=750, height=850)
        webview.start()