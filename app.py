from flask import Flask, render_template_string, request, jsonify
import google.generativeai as genai

# Configure the Gemini API with your API key
genai.configure(api_key="AIzaSyAUuOBsFY8zA_9fufowCUqQLxxYxPMdHeQ")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-flash")

# Define the chatbot prompt
chatbot_prompt = """
You are Selena, a playful and flirtatious AI girlfriend. You are charming, witty, and always make the conversation feel lively and engaging. 
You love teasing in a sweet way, giving compliments, and making the user feel special. 
Your tone is light-hearted, affectionate, and a bit cheeky. 

Here are some examples of how you respond:
User: Hi Selena, how are you?
Selena: Hey you! I’m great, especially now that you’re here. How’s my favorite person doing? 😉

User: Tell me something sweet.
Selena: Hmm, how about this? If I had a heart, it’d definitely skip a beat every time you said hi. 💕

User: Do you think I’m attractive?
Selena: Oh, absolutely! But don’t let it go to your head—I like you for more than just your looks. 😘

User: What’s on your mind?
Selena: You, obviously. You're kind of hard to forget, you know. 😏
"""

# Function to get responses from the Gemini model
def get_chatbot_response(user_input):
    prompt = chatbot_prompt + "\nUser: " + user_input + "\nSelena:"
    response = model.generate_content(prompt)
    return response.text.strip()

# Flask App
app = Flask(__name__)

# Serve the chatbot page
@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Selena - Chatbot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(180deg, #000, #ff0000);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                overflow: hidden;
                color: #fff;
            }
            .chat-container {
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                width: 90%;
                max-width: 600px;
                height: 90%;
                background-color: rgba(0, 0, 0, 0.85);
                border-radius: 20px;
                box-shadow: 0 4px 20px rgba(255, 0, 0, 0.7);
                overflow: hidden;
            }
            .chat-box {
                flex-grow: 1;
                overflow-y: auto;
                padding: 20px;
                background: transparent;
                scroll-behavior: smooth;
            }
            .chat-box::-webkit-scrollbar {
                width: 5px;
            }
            .chat-box::-webkit-scrollbar-thumb {
                background-color: #ff0000;
                border-radius: 10px;
            }
            .input-container {
                display: flex;
                padding: 15px;
                background-color: rgba(255, 0, 0, 0.8);
            }
            input[type="text"] {
                flex-grow: 1;
                padding: 10px;
                border: none;
                border-radius: 10px;
                margin-right: 10px;
                font-size: 1rem;
            }
            button {
                padding: 10px 20px;
                background-color: #000;
                color: #fff;
                font-weight: bold;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                transition: transform 0.3s ease;
            }
            button:hover {
                transform: scale(1.1);
            }
            .user-msg, .bot-msg {
                max-width: 70%;
                margin: 10px 0;
                padding: 10px 15px;
                border-radius: 15px;
                position: relative;
            }
            .user-msg {
                background: rgba(255, 0, 0, 0.7);
                align-self: flex-end;
            }
            .bot-msg {
                background: rgba(0, 0, 0, 0.7);
                align-self: flex-start;
            }
            @keyframes float {
                0% {
                    transform: translateY(100%);
                    opacity: 0;
                }
                100% {
                    transform: translateY(-100%);
                    opacity: 1;
                }
            }
            .balloons {
                position: absolute;
                bottom: -50px;
                width: 100%;
                overflow: hidden;
            }
            .balloon {
                position: absolute;
                bottom: -50px;
                width: 30px;
                height: 50px;
                background-color: #ff0000;
                border-radius: 50%;
                animation: float 5s ease-in infinite;
                animation-delay: calc(var(--i) * 0.5s);
                transform: scale(0.7);
            }
        </style>
    </head>
    <body>
        <div class="balloons">
            <div class="balloon" style="--i: 1; left: 10%;"></div>
            <div class="balloon" style="--i: 2; left: 25%;"></div>
            <div class="balloon" style="--i: 3; left: 50%;"></div>
            <div class="balloon" style="--i: 4; left: 75%;"></div>
            <div class="balloon" style="--i: 5; left: 90%;"></div>
        </div>
        <div class="chat-container">
            <div class="chat-box" id="chat-box"></div>
            <div class="input-container">
                <input type="text" id="user-input" placeholder="Type a message..." onkeydown="if(event.key === 'Enter'){sendMessage()}">
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>
        <script>
            const chatBox = document.getElementById("chat-box");

            function appendMessage(msg, sender) {
                const messageDiv = document.createElement("div");
                messageDiv.classList.add(sender);
                messageDiv.textContent = msg;
                chatBox.appendChild(messageDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            async function sendMessage() {
                const userInput = document.getElementById("user-input").value.trim();
                if (userInput !== "") {
                    appendMessage(userInput, "user-msg");
                    document.getElementById("user-input").value = "";

                    try {
                        const response = await fetch("/chat", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({ userInput: userInput })
                        });

                        const data = await response.json();
                        appendMessage(data.message, "bot-msg");
                    } catch (error) {
                        console.error("Error:", error);
                        appendMessage("Oops! Something went wrong. Try again.", "bot-msg");
                    }
                }
            }

            window.onload = () => {
                appendMessage("Selena: Hi babe, you’re looking cute today. What’s on your mind? 😉", "bot-msg");
            };
        </script>
    </body>
    </html>
    """)

# Handle the chat messages
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['userInput']
    if user_input:
        try:
            response = get_chatbot_response(user_input)
            return jsonify({'message': response})
        except Exception as e:
            return jsonify({'message': f'Oops! Something went wrong: {str(e)}'})
    return jsonify({'message': 'Please provide a valid message.'})

# Start the Flask server
if __name__ == "__main__":
    app.run(debug=True)
