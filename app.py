from flask import Flask, request, jsonify, render_template_string
import requests
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is the Product Research App!"

@app.route('/api/trends/<keyword>', methods=['GET'])
def get_trends(keyword):
    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list = [keyword]
    pytrends.build_payload(kw_list, cat=0, timeframe='now 7-d', geo='', gprop='')
    trends = pytrends.interest_over_time()
    if not trends.empty:
        plt.figure(figsize=(10,5))
        trends[keyword].plot()
        plt.title(f'Trends for {keyword}')
        plt.xlabel('Date')
        plt.ylabel('Interest')
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()  # Bu satır ile grafiği kapatıyoruz
        return render_template_string('<img src="data:image/png;base64,{{ plot_url }}">', plot_url=plot_url)
    else:
        return jsonify({"error": "No data found"}), 404

if __name__ == '__main__':
    app.run(debug=True)