/* * chatbot.js - API INTEGRATION & SESSION PERSISTENCE VERSION
 * This file handles the UI, API communication, and saves/loads conversation history.
 */
const BASE_URL = window.getApiBaseUrl();
const HISTORY_KEY = 'calmpulse_chat_history';

// Helper to save the current chat content to session storage
function saveChatHistory() {
    const chatBody = document.getElementById('chatbot-body');
    if (chatBody) {
        sessionStorage.setItem(HISTORY_KEY, chatBody.innerHTML);
    }
}

// Helper to load chat content from session storage
function loadChatHistory(defaultMessage) {
    const savedHistory = sessionStorage.getItem(HISTORY_KEY);
    if (savedHistory) {
        return savedHistory;
    }
    // If no history is found, return the default welcome message
    return `<div class="message bot-message">${defaultMessage}</div>`;
}

function initializePageChatbot(userRole) {
    
    const containerElement = document.getElementById('chat-page-container');
    if (!containerElement) {
        console.error("Chat page container not found. Check chat.html structure.");
        return;
    }

    // Define the default welcome message
    const initialMessage = `Hello! I'm your CalmPulse AI. I see you are a ${userRole}. I can give you advice about stress and coping mechanisms.`;

    // ----------------------------------------------------
    // I. Inject Chat UI into the dedicated container
    // ----------------------------------------------------
    const chatUIHTML = `
        <div class="chatbot-container-full" id="chatbot-container">
            <div class="chatbot-header">Pulse Bot 🤖</div>
            <div class="chatbot-body" id="chatbot-body">
                </div>
            <div class="chatbot-footer">
                <input type="text" id="chatbot-input" placeholder="Ask me about stress..." class="full-width-input">
                <button id="chatbot-send-btn">Send</button>
            </div>
        </div>
    `;
    
    containerElement.innerHTML = chatUIHTML;

    // ----------------------------------------------------
    // II. DOM References and Load History
    // ----------------------------------------------------
    const chatbotBody = document.getElementById('chatbot-body');
    const chatbotInput = document.getElementById('chatbot-input');
    const chatbotSendBtn = document.getElementById('chatbot-send-btn');
    let isTyping = false;
    
    // Load existing history or the default message
    chatbotBody.innerHTML = loadChatHistory(initialMessage);


    const scrollToBottom = () => { chatbotBody.scrollTop = chatbotBody.scrollHeight; };
    const appendMessage = (text, sender) => {
        const msgEl = document.createElement('div');
        msgEl.classList.add('message', `${sender}-message`);
        msgEl.textContent = text;
        chatbotBody.appendChild(msgEl);
        scrollToBottom();
        saveChatHistory(); // Save immediately after appending a new message
    };

    // ----------------------------------------------------
    // III. API Request Function (Unchanged logic)
    // ----------------------------------------------------
    async function getApiResponse(userMessage) {
        if (isTyping) return;
        isTyping = true;
        
        // Disable input and show typing indicator
        chatbotInput.disabled = true;
        chatbotSendBtn.disabled = true;
        appendMessage('Pulse Bot is thinking...', 'bot');
        const typingIndicator = chatbotBody.lastChild;

        try {
            const response = await fetch(`${BASE_URL}/chat_api`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    message: userMessage,
                    user_role: userRole
                })
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.statusText}`);
            }

            const data = await response.json();
            
            // Remove typing indicator and display response
            chatbotBody.removeChild(typingIndicator); 
            appendMessage(data.response || "Sorry, I couldn't get a response.", 'bot');

        } catch (error) {
            console.error('Chat API Error:', error);
            if (chatbotBody.contains(typingIndicator)) {
                chatbotBody.removeChild(typingIndicator);
            }
            appendMessage("Connection error: Could not reach the AI server. Check your Flask server.", 'bot');
        } finally {
            // Re-enable input
            chatbotInput.disabled = false;
            chatbotSendBtn.disabled = false;
            chatbotInput.focus();
            isTyping = false;
        }
    }

    // ----------------------------------------------------
    // IV. Main Send Logic and Event Listeners
    // ----------------------------------------------------
    function sendMessage() {
        const userText = chatbotInput.value.trim();
        if (userText === '' || isTyping) return;

        appendMessage(userText, 'user');
        getApiResponse(userText);
        chatbotInput.value = '';
    }

    chatbotSendBtn.addEventListener('click', sendMessage);
    chatbotInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault(); 
            sendMessage();
        }
    });

    // Save history just before the user leaves the page or navigates
    window.addEventListener('beforeunload', saveChatHistory);
}
