const token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDUzNjIwNTUsImlhdCI6MTYwNTM1NDg1NX0.ekKbg1hMln0fjHh51QdEZ4nckJ3XP5o6hulOJjBtOko"

const chatSocket = new WebSocket(
    'ws://'
    + 'localhost:8000/messages?token='
    + token
    + '&receiver_username=uchencho'
    +'&receiver_id=1'
);


chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data)
    console.log(data, "and", data.message, ", and again", data.message.message)
    document.querySelector('#chat-log').value += (data.message.message + '\n');
};

chatSocket.onclose = function(e) {
    console.error("Chat socket closed unexpectedly");
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {
        document.querySelector("#chat-message-submit").click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message' : message
    }));
    messageInputDom.value = '';
};
