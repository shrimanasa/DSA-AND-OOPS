from flask import Flask, render_template, request
import pandas as pd

app = Flask(_name_)

# ---------- Trie Classes ----------
class TrieNode:
    def _init_(self):
        self.children = {}
        self.is_end = False
        self.hashtag_info = None

class Trie:
    def _init_(self):
        self.root = TrieNode()

    def insert(self, hashtag, rank, info):
        node = self.root
        for char in hashtag:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.hashtag_info = {'rank': rank, 'info': info}

    def search(self, hashtag):
        node = self.root
        for char in hashtag:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.hashtag_info if node.is_end else None

    def starts_with(self, prefix):
        def dfs(node, prefix, results):
            if node.is_end:
                results.append({'hashtag': '#' + prefix, 'rank': node.hashtag_info['rank'], 'info': node.hashtag_info['info']})
            for char, next_node in node.children.items():
                dfs(next_node, prefix + char, results)

        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        results = []
        dfs(node, prefix, results)
        return results[:5]

# ---------- Load data and build Trie ----------
df = pd.read_csv('hashtag_data.csv')
df['Hashtag'] = df['Hashtag'].astype(str).str.lower().str.lstrip('#')
df = df.dropna(subset=['Hashtag', 'Information'])

trie = Trie()
for idx, row in df.iterrows():
    trie.insert(row['Hashtag'], idx + 1, row['Information'])

# ---------- Flask Routes ----------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    hashtag = request.form['hashtag'].strip()
    hashtag_clean = hashtag.lstrip('#').lower()

    exact = trie.search(hashtag_clean)

    if exact:
        return render_template('index.html', result=True, hashtag="#" + hashtag_clean,
                               rank=exact['rank'], info=exact['info'])
    else:
        suggestions = trie.starts_with(hashtag_clean[:4])  # Try with first 4 letters
        return render_template('index.html', result=False, hashtag="#" + hashtag_clean,
                               suggestions=suggestions)

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5001, debug=True)