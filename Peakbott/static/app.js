class Chatbox {
    constructor() {
        console.log("Chatbox initialized");  
        this.args = {
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        };

        this.messages = [];
    }

    display() {
        const {chatBox, sendButton} = this.args;        
        sendButton.addEventListener('click', () => this.onSendButton(chatBox));        
        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        });
    }
    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value;
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 };
        this.messages.push(msg1);
        
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
        })
        .then(r => r.json())
        .then(r => {
            if (r.music) {
                this.displayMusic(r.music);
                this.messages.push({ name: "PeakBot", message: r.message });
            } else {
                let msg2 = { name: "PeakBot", message: r.answer };
                this.messages.push(msg2);
            }
            this.updateChatText(chatbox);
            textField.value = '';
        })
        .catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox);
            textField.value = '';
        });
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item) {
            if (item.name === "PeakBot") {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
            } else {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
            }
        });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
    
    displayResponse(response) {
    const chatboxMessages = document.querySelector('.chatbox__messages');
    const responseElement = document.createElement('div');
    responseElement.classList.add('chatbot-message'); 
    responseElement.innerHTML = response; 
    chatboxMessages.appendChild(responseElement);
}  
}
const chatbox = new Chatbox();
chatbox.display();
