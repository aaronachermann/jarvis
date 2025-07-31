"""Simple web dashboard to toggle tools and features at runtime."""
from flask import Flask, request, redirect, url_for, render_template_string
from config import ENABLED_TOOLS, FEATURE_FLAGS

app = Flask(__name__)

PAGE = """
<h1>Jarvis Dashboard</h1>
<form method='post'>
<h2>Tools</h2>
{% for name, enabled in tools.items() %}
<label><input type='checkbox' name='tool_{{name}}' {% if enabled %}checked{% endif %}> {{name}}</label><br>
{% endfor %}
<h2>Features</h2>
{% for name, enabled in features.items() %}
<label><input type='checkbox' name='feature_{{name}}' {% if enabled %}checked{% endif %}> {{name}}</label><br>
{% endfor %}
<button type='submit'>Save</button>
</form>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        for name in list(ENABLED_TOOLS.keys()):
            ENABLED_TOOLS[name] = f'tool_{name}' in request.form
        for name in list(FEATURE_FLAGS.keys()):
            FEATURE_FLAGS[name] = f'feature_{name}' in request.form
        return redirect(url_for('index'))
    return render_template_string(PAGE, tools=ENABLED_TOOLS, features=FEATURE_FLAGS)

if __name__ == '__main__':
    app.run(port=5000)

