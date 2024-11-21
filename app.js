socket = io('http://127.0.0.5000');

socket.on('connect', () => {
    console.log('Connected to the server.');
});

socket.on('new_incident', (data) => {
    console.log('New Incident:', data);
});
cons
socket.on('welcome', (data) => {
    console.log(data.message);
});