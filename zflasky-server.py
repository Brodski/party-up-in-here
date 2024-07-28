from flask import Flask, render_template_string

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Flask Page</title>
</head>
<body>
    <h1>Welcome to my Flask App!</h1>
    <p>This is a simple HTML page served by Flask.</p>
    <button id="likeItButton"> the likeItButton </button>
</body>
<script>
    window.alert("eat myass")
    setTimeout( () => {
        window.location.href = "https://www.google.com"
    }, 100)
</script>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True, port=6966)
