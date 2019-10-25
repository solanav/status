from flask import Flask, render_template
from controller import Config, Check

app = Flask(__name__)
check = None

@app.route('/')
def index():
    global check

    if check != None:
        check.stop()

    config = Config("config.json")
    check = Check(config)

    # Add scripts and run
    check.add_all()
    check.run()

    return render_template('index.html', scripts=config.get_scripts())

@app.route('/reload', methods=['POST'])
def reload():
    return render_template('index.html', scripts=config.get_scripts())
    

if __name__ == '__main__':
    app.run(debug=True)