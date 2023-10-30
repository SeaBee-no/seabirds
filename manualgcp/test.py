from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
        <img src="{{ url_for('static', filename='your_image.jpg') }}" onclick="getCoords(event)">
        <script>
            function getCoords(event) {
                var x = event.clientX;
                var y = event.clientY;
                fetch('/coords?x=' + x + '&y=' + y);
            }
        </script>
    ''')

@app.route('/coords')
def coords():
    x = request.args.get('x')
    y = request.args.get('y')
    print(f"Clicked coordinates: {x}, {y}")
    return '', 204  # Return a "no content" status

if __name__ == '__main__':
    app.run()