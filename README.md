# URL Link Checker
詳しくはリポジトリ内の　Internal url searcher.pptx　を参照

![image](https://github.com/user-attachments/assets/1d6202c6-f1e0-4bbc-8abf-9f8cf80478d8)

# OverView 
入力されたurlの内部リンクを検索し、有効でないものや内部リンク数を可視化するwebアプリケーション

# Requirements
* Flask 3.03
* Python 3.10

# Usage
1. http://unison-app.online/  へアクセス
2. https://unison-career.com/engineer-media/ から始まるurlを入力 (余計なurlが出力されないようにフィルタリング済)
3. 404などページが存在しないNodeはグレーに表示される
4. 右上の検索欄からurlに含まれる数字や英単語の検索が可能
5. Nodeにカーソルを合わせると、左下にページのスクリーンショットが表示される
6. Nodeをクリックし、最大15s待機すると、クリックしたNodeを中心に内部リンクを検索可能

# Discription

<img width="630" alt="image" src="https://github.com/user-attachments/assets/76718b3b-5397-41cd-9349-62ea4e91f482" />

ポート番号を分け、リバースプロキシサーバーを使用することで、Node.jsとPythonの機能を分割可能
