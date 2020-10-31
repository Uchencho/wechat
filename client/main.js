const token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDQxNjUyMTMsImlhdCI6MTYwNDE1ODAxM30.6N0iUZuo6jf3VdnszZSGGmi3Ob8yE5Hyk4A4UK2b75M"

const chatSocket = new WebSocket(
    'ws://'
    + 'localhost:8000/messages?token='
    + token
);

chatSocket.onopen = function(e) {
    chatSocket.send(JSON.stringify({
        'text' : {
            'receiver_username' : "Uchenchooo",
            'receiver_id' : 4
        }
    }))
};

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data)
    document.querySelector('#chat-log').value += (data.message + '\n');
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
