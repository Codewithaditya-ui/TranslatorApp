import webview
import threading
import time
from pywebio.input import textarea, select
from pywebio.output import put_text, put_html, clear, use_scope
from deep_translator import GoogleTranslator
from pywebio.platform.flask import webio_view
from flask import Flask

app = Flask(__name__)

def translator_logic():
    # Improved Visuals & Bolder Text
    put_html("""
    <style>
        body { background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d); min-height: 100vh; color: white; font-family: 'Arial Black'; }
        .app-container { background: rgba(0,0,0,0.6); padding: 30px; border-radius: 20px; max-width: 600px; margin: 40px auto; border: 2px solid #fff; }
        h1 { font-size: 3em; text-align: center; margin-bottom: 20px; }
        .result-area { background: #fff; color: #000; padding: 15px; border-radius: 10px; margin-top: 20px; font-weight: 900; }
    </style>
    """)

    put_html("<div class='app-container'>")
    put_html("<h1>ADITYA'S APP</h1>")
    
    while True:
        text = textarea("ENTER TEXT", placeholder="Type here...")
        
        langs = {
            'HINDI': 'hindi', 'BENGALI': 'bengali', 'ODIA': 'odia', 
            'PUNJABI': 'punjabi', 'ENGLISH': 'english', 'FRENCH': 'french'
        }
        
        target = select("SELECT LANGUAGE", list(langs.keys()))
        
        # This part handles the translation
        with use_scope('res', clear=True):
            put_text("Translating... Please wait.")
            try:
                translated = GoogleTranslator(source='auto', target=langs[target]).translate(text)
                clear('res')
                put_html(f"""
                <div class='result-area'>
                    <span style='color:red;'>ORIGINAL:</span> {text}<br>
                    <span style='color:blue;'>{target}:</span> {translated}
                </div>
                """)
            except Exception as e:
                clear('res')
                put_text(f"Error: Make sure you are connected to the Internet!")

# Integration
app.add_url_rule('/', 'webio_view', webio_view(translator_logic), methods=['GET', 'POST', 'OPTIONS'])

def run_server():
    # We use port 5005 to avoid the "address in use" error
    app.run(port=5005, debug=False, threaded=True)

if __name__ == '__main__':
    # 1. Start Server in background
    t = threading.Thread(target=run_server)
    t.daemon = True
    t.start()

    # 2. Wait for server to wake up
    time.sleep(3)

    # 3. Open the App Window
    webview.create_window("Aditya's Translator", "http://127.0.0.1:5005", width=700, height=800)
    webview.start()