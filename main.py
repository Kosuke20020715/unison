from flask import Flask, jsonify, request, render_template
import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def search_link(url, timeout=5):
    """指定されたURL内の特定パターンのリンクを収集し、リストとその数を返します。"""
    try:
        link_list = []
        res = requests.get(url, timeout=timeout)  # タイムアウトを設定
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")
        links = soup.select("a")
        for link in links:
            link_url = link.get("href")
            if link_url and re.search(r"https://unison-career.com/engineer-media/", link_url):
                link_list.append(link_url)
        return list(set(link_list)), len(set(link_list))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return [], 0  # エラーが発生した場合は空のリストとカウント0を返します

def fetch_link_count(link):
    """リンクのリンク数を取得するためのヘルパー関数。"""
    return search_link(link)[1]

def prior(url):
    """収集したリンクを並列処理でリンク数でソートし、ソート済みリストとリンク数を返します。"""
    try:
        link_results, _ = search_link(url)
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_to_link = {executor.submit(fetch_link_count, link): link for link in link_results}
            sorted_links = sorted(
                ((future.result(), future_to_link[future]) for future in as_completed(future_to_link)),
                reverse=True
            )
        return [num for num, _ in sorted_links], [link for _, link in sorted_links]
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return [], []  # エラーが発生した場合は空のリストを返します

@app.route("/")
def index():
    """ホームページをレンダリングします。"""
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400

    try:
        link_counts, sorted_links = prior(url)
        data = [{"url": link, "count": count} for link, count in zip(sorted_links, link_counts)]
        response = jsonify({"center_url": url, "links": data})
        response.headers.add("Access-Control-Allow-Origin", "*")  # CORSヘッダーを追加
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
