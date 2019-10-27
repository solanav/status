from flask import Flask, render_template
from controller import Config, Check
from flask_socketio import SocketIO, emit
from threading import Timer

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    # Get the script list
    scripts = config.get_scripts()
    status_script_list = []

    up = 0
    down = 0
    warning = 0
    unknown = 0

    # Append status of script each time this is reloaded
    for script in scripts:
        script['status'] = check.state[script['name']]
        status_script_list.append(script)

        if script['status'] == 'UP':
            up += 1
        elif script['status'] == 'DOWN':
            down += 1
        elif script['status'] == 'WARNING':
            warning += 1
        else:
            unknown += 1

    stats = {}
    stats['up'] = up
    stats['down'] = down
    stats['warning'] = warning
    stats['unknown'] = unknown

    return render_template('index.html', scripts=status_script_list, stats=stats)

@socketio.on('reload')
def resp():
    script_dict = config.get_scripts()

    up = 0
    down = 0
    warning = 0
    unknown = 0

    for script in script_dict:
        status = check.state[script['name']]
        if status == 'UP':
            up += 1
        elif status == 'DOWN':
            down += 1
        elif status == 'WARNING':
            warning += 1
        else:
            unknown += 1

    stats = {}
    stats['up'] = up
    stats['down'] = down
    stats['warning'] = warning
    stats['unknown'] = unknown

    for script in script_dict:
        emit('update_status', {'stats': stats, 'name': script['name'], 'status': check.state[script['name']]})

if __name__ == '__main__':
    config = Config("config.json")
    check = Check(config)
    client = None

    check.add_all()
    check.run()

    socketio.run(app)