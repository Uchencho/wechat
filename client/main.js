const token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2MDQxNzg4NTIsImlhdCI6MTYwNDE3MTY1Mn0.T9g2hJCi2u3YLp9jvUtOOdHIoR_jKzBmkLpBmE-Pzfg"

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
