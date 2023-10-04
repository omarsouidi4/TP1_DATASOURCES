from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    variable="""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-TP5LRMBZ8T"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-TP5LRMBZ8T');
</script>"""
    return "<p>ALLEZ L'OM!</p>" + variable
