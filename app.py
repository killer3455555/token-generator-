from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Simple HTML Form
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Facebook Token Generator</title>
    <style>
        body { font-family: Arial; background: #111; color: #fff; text-align: center; }
        .box { margin: 100px auto; padding: 30px; width: 400px; background: #222; border-radius: 10px; }
        input { width: 90%; padding: 10px; margin: 10px 0; border-radius: 5px; border: none; }
        button { padding: 10px 20px; background: green; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .token { background: #333; padding: 10px; border-radius: 5px; word-wrap: break-word; }
    </style>
</head>
<body>
    <div class="box">
        <h2>🔑 Facebook Token Generator</h2>
        <form method="post">
            <input type="text" name="app_id" placeholder="Enter App ID" required><br>
            <input type="text" name="app_secret" placeholder="Enter App Secret" required><br>
            <button type="submit">Generate Token</button>
        </form>
        {% if token %}
        <h3>✅ Access Token:</h3>
        <div class="token">{{ token }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    token = None
    if request.method == "POST":
        app_id = request.form.get("app_id")
        app_secret = request.form.get("app_secret")

        url = "https://graph.facebook.com/oauth/access_token"
        params = {
            "client_id": app_id,
            "client_secret": app_secret,
            "grant_type": "client_credentials"
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            token = response.json().get("access_token")
        else:
            token = "❌ Error: " + response.text

    return render_template_string(html, token=token)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
