$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/');

    socket.on('update_status', function(data) {
        state = document.getElementById(data.name);
        state.innerHTML = data.status;
        if (data.status == 'ERROR') {
            state.style.color = 'red';
        } else {
            state.style.color = 'green';
        }
    });
    
    (function(){
        socket.emit('reload');
        setTimeout(arguments.callee, 1000);
    })();
});
