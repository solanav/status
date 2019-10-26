from flask import Flask, render_template, redirect
from controller import Config, Check
from flask_socketio import SocketIO, emit
from threading import Timer

app = Flask(__name__)
socketio = SocketIO(app)
config = Config("config.json")
check = Check(config)
run_once = 0
client = None

@app.route('/')
def index():
    global run_once
    
    # Only run scripts on first run
    if run_once == 0:
        run_once = 1

        # Add scripts and run
        check.add_all()
        check.run()
    
    # Get the script list
    scripts = config.get_scripts()
    status_script_list = []

    # Append status of script each time this is reloaded
    for script in scripts:
        script['status'] = check.state[script['name']]
        status_script_list.append(script)

    return render_template('index.html', scripts=status_script_list)

@socketio.on('reload')
def resp():
    script_dict = config.get_scripts()
    for script in script_dict:
        emit('update_status', {'name': script['name'], 'status': check.state[script['name']]})

if __name__ == '__main__':
    socketio.run(app)