document.addEventListener('DOMContentLoaded', () => {
    // DOM elements
    const chatbotOuterContainer = document.getElementById('chatbot-outer-container');
    const chatbotContainer = document.getElementById('chatbot-container');
    const chatbotMessages = document.getElementById('chatbot-messages');
    const messageWrapper = document.getElementById('message-wrapper');
    const chatbotInput = document.getElementById('chatbot-input-field');
    const chatbotSend = document.getElementById('chatbot-send');
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotOpen = document.getElementById('chatbot-open');
    const chatbotInputContainer = document.getElementById('chatbot-input');

    // Debug: Verify DOM elements
    console.log('DOM elements loaded:', {
        chatbotOuterContainer,
        chatbotContainer,
        chatbotMessages,
        messageWrapper,
        chatbotInput,
        chatbotSend,
        chatbotToggle,
        chatbotOpen,
        chatbotInputContainer
    });

    if (!chatbotOuterContainer || !chatbotContainer || !chatbotMessages || !messageWrapper || !chatbotInput || !chatbotSend || !chatbotToggle || !chatbotOpen || !chatbotInputContainer) {
        console.error('One or more DOM elements are missing. Check index.html for correct IDs.');
        return;
    }

    // Ensure chatbot is hidden and open button is visible on page load
    chatbotOuterContainer.style.display = 'none';
    chatbotContainer.style.display = 'none';
    chatbotOpen.style.display = 'inline-flex';
    chatbotToggle.classList.add('minimized');
    chatbotToggle.setAttribute('aria-label', 'Expand chatbot'); // Initial state
    let isFirstOpen = true;

    // Show chatbot when open button is clicked
    chatbotOpen.addEventListener('click', () => {
        console.log('Chat button clicked');
        chatbotOuterContainer.style.display = 'block';
        chatbotContainer.style.display = 'flex';
        chatbotOpen.style.display = 'none';
        chatbotToggle.classList.remove('minimized');
        chatbotToggle.setAttribute('aria-label', 'Minimize chatbot');
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;

        // Show welcome message on first open
        if (isFirstOpen) {
            setTimeout(() => {
                const welcomeDiv = document.createElement('div');
                welcomeDiv.classList.add('welcome-message');
                welcomeDiv.innerHTML = '<i class="fas fa-plane-departure"></i> Welcome to your Travel Assistant!';
                messageWrapper.appendChild(welcomeDiv);

                setTimeout(() => {
                    appendMessage('assistant', 'Hello! I’m here to help plan your perfect trip. Where would you like to go?', '<i class="fas fa-suitcase"></i>');
                }, 1000);
            }, 500);
            isFirstOpen = false;
        }
    });

    // Toggle chatbot visibility (close/minimize)
    chatbotToggle.addEventListener('click', () => {
        console.log('Toggle button clicked');
        if (chatbotContainer.style.display === 'flex') {
            chatbotOuterContainer.style.display = 'none';
            chatbotContainer.style.display = 'none';
            chatbotOpen.style.display = 'inline-flex';
            chatbotToggle.classList.add('minimized');
            chatbotToggle.setAttribute('aria-label', 'Expand chatbot');
        } else {
            chatbotOuterContainer.style.display = 'block';
            chatbotContainer.style.display = 'flex';
            chatbotOpen.style.display = 'none';
            chatbotToggle.classList.remove('minimized');
            chatbotToggle.setAttribute('aria-label', 'Minimize chatbot');
        }
    });

    // Send message
    const sendMessage = async () => {
        const message = chatbotInput.value.trim();
        if (!message) {
            console.log('No message entered');
            return;
        }

        console.log('Sending message:', message);

        // Add user message
        appendMessage('user', message, '<i class="fas fa-user"></i>');
        chatbotInput.value = '';

        // Show typing indicator
        const typingIndicator = document.createElement('div');
        typingIndicator.classList.add('typing-indicator');
        typingIndicator.innerHTML = 'Travel Assistant is typing... <span class="dot"></span><span class="dot"></span><span class="dot"></span>';
        messageWrapper.appendChild(typingIndicator);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;

        try {
            const payload = { message, user_id: "guest" };
            console.log('Fetch payload:', payload);

            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            console.log('Fetch response status:', response.status);
            console.log('Fetch response:', response);

            // Remove typing indicator
            typingIndicator.remove();

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Fetch data:', data);

            if (data.error) {
                appendMessage('assistant', 'Sorry, something went wrong: ' + data.error, '<i class="fas fa-suitcase"></i>');
            } else {
                appendMessage('assistant', data.response, '<i class="fas fa-suitcase"></i>');
            }
        } catch (error) {
            typingIndicator.remove();
            console.error('Fetch error:', error);
            appendMessage('assistant', 'Error connecting to the Travel Assistant: ' + error.message, '<i class="fas fa-suitcase"></i>');
        }

        // Scroll to bottom
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    };

    // Append message to chat
    const appendMessage = (role, content, avatar) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${role}-message`);
        const label = role === 'user' ? '🧑 User' : '🧳 Travel Assistant';
        messageDiv.innerHTML = `
            <div class="message-header">${label}</div>
            <div class="message-content">${content}</div>
        `;
        messageWrapper.appendChild(messageDiv);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        console.log(`Message appended (${role}):`, content);
    };

    // Handle send button click
    chatbotSend.addEventListener('click', () => {
        console.log('Send button clicked');
        sendMessage();
    });

    // Handle Enter key
    chatbotInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            console.log('Enter key pressed');
            sendMessage();
        }
    });
});