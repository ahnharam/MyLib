from flask import Flask
import threading

def run_webserver():
    app = Flask(__name__)

    @app.route("/healthz")
    def health():
        return "OK", 200

    def run():
        app.run(host="0.0.0.0", port=10000)

    threading.Thread(target=run, daemon=True).start()
