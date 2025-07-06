from flask import Flask, request, jsonify
from flask_cors import CORS
from cachetools import TTLCache
import lib2
import json
import asyncio

app = Flask(__name__)
CORS(app)
cache = TTLCache(maxsize=100, ttl=300)

# Vercel requires an explicit `application` variable for serverless environments
application = app  # Important for Vercel to recognize the WSGI app

@app.route('/api/account')
def get_account_info():
    region = request.args.get('region')
    uid = request.args.get('uid')
    
    if not uid:
        return jsonify({"error": "UID is required"}), 400
    
    if not region:
        return jsonify({"error": "Region is required"}), 400

    try:
        return_data = asyncio.run(lib2.GetAccountInformation(uid, "7", region, "/GetPlayerPersonalShow"))
        return jsonify(return_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
