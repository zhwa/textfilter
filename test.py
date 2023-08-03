import requests
from collections import Counter
from filters import TextFilter
import plotly.graph_objects as go

filter = TextFilter()
words = []

url = "https://www.gutenberg.org/cache/epub/1513/pg1513.txt"
response = requests.get(url)
text_content = response.content.decode("utf-8")
sentences = text_content.split('\n')
for sentence in sentences:
    pure_text = sentence.replace('\n', '').replace('\r', '')
    if len(pure_text) == 0:
        continue
    if filter.contains_privacy(pure_text) or filter.is_offsensive(pure_text) or not filter.is_language(pure_text, "en-us"):
        continue
    words.extend(pure_text.split())

word_counts = Counter(words)
x_values = list(word_counts.keys())
y_values = list(word_counts.values())

fig = go.Figure([go.Bar(x=x_values, y=y_values)])
fig.show()