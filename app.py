from flask import Flask, render_template
from controller import Config, Check
from flask_socketio import SocketIO, emit
from threading import Timer
from pprint import pprint

app = Flask(__name__)
socketio = SocketIO(app)
config = Config("config.json")
check = Check(config)
client = None

@app.route('/')
def index():
    # Get the script list with state and stats
    status_script_list, stats = check.get_all_info()

    return render_template('index.html', scripts=status_script_list, stats=stats)

@socketio.on('reload')
def resp():
    status_script_list, stats = check.get_all_info()

    for script in status_script_list:
        print("Sending updated data:")
        pprint({'stats': stats, 'name': script['name'], 'status': check.state[script['name']]})
        emit('update_status', {'stats': stats, 'name': script['name'], 'status': check.state[script['name']]})
        print()

if __name__ == '__main__':
    check.add_all()
    check.run()

    socketio.run(app)