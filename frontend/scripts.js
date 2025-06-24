
const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// Common greetings and responses
const greetings = {
    hi: "Hello! Welcome to APask Vidya. Ask me about colleges in Andhra Pradesh!",
    hello: "Namaste! How can I help you with college info today?",
    hey: "Hey there! Ready to explore engineering colleges?",
    "good morning": "Good morning! Let's find the perfect college for you!",
    "good evening": "Good evening! Ask away about courses, fees, or placements!"
};

// Fallback jokes for unrecognized queries
const jokes = [
    "Why did the computer go to college? It wanted to be a 'byte'-sized scholar! 😄 Try a suggested prompt below.",
    "What do you call a student who loves coding? A 'digital dreamer'! 🤖 Try one of these prompts.",
    "Why was the math book sad? Too many problems! 📚 Check out these suggested questions."
];

// Suggested prompts for unrecognized queries
const suggestedPrompts = [
    "What are the courses at SRM University?",
    "What are the courses at sample?",
    "Which courses are offered by SRM University?",
    "Which courses are offered by sample?",
    "List the courses available at SRM University.",
    "List the courses available at sample.",
    "What are the programs at SRM University?",
    "Which programs are offered by SRM University?",
    "List all available courses at SRM?",
    "What is the convener quota fee at SRM University?",
    "What is the convener quota fee at sample?",
    "How much is the annual fee for convener quota at SRM University?",
    "How much is the annual fee for convener quota at sample?",
    "Tell me the convener quota fees for SRM University.",
    "Tell me the convener quota fees for sample.",
    "What is the management quota fee at SRM University?",
    "What is the management quota fee at sample?",
    "How much is the management quota fee at SRM University?",
    "How much is the management quota fee at sample?",
    "Tell me the management quota fees for SRM University.",
    "Tell me the management quota fees for sample.",
    "What is the placement percentage at SRM University?",
    "What is the placement percentage at sample?",
    "How good are placements at SRM University?",
    "How good are placements at sample?",
    "Tell me about SRM University placements.",
    "Tell me about sample placements.",
    "What is the contact number for SRM University?",
    "What is the contact number for sample?",
    "How can I contact SRM University?",
    "How can I contact sample?",
    "Give me the phone number of SRM University.",
    "Give me the phone number of sample.",
    "Tell me about SRM University.",
    "Tell me about sample.",
    "What are the details of SRM University?",
    "What are the details of sample?",
    "Give me information about SRM University.",
    "Give me information about sample."
];

// Multiple fallback messages for errors
const errorFallBacks = [
    "Oops, looks like my circuits got tangled! 🛠️ Please try again in a moment.",
    "Yikes, the server took a coffee break! ☕ Check your connection and retry.",
    "Something's gone haywire in the cloud! 🌩️ Ask again or try a different question."
];

// Track fallback index for sequential error messages
let errorFallbackIndex = 0;

function addMessage(message, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.className = isUser ? 'user-message self-end bg-indigo-600 text-white rounded-lg p-2 m-2 max-w-xs' : 'bot-message bg-gray-800 text-white rounded-lg p-2 m-2 max-w-xs';
    messageDiv.innerHTML = message.replace(/\n/g, '<br>'); // Handle newlines
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function getRandomSuggestions(count = 3) {
    // Shuffle and pick 'count' random prompts
    const shuffled = [...suggestedPrompts].sort(() => Math.random() - 0.5);
    return shuffled.slice(0, count).map(prompt => `<li>${prompt}</li>`).join('');
}

async function fetchJoke() {
    try {
        const response = await fetch('https://v2.jokeapi.dev/joke/Programming?type=single');
        const data = await response.json();
        return data.joke || jokes[Math.floor(Math.random() * jokes.length)];
    } catch {
        return jokes[Math.floor(Math.random() * jokes.length)];
    }
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, true);
    userInput.value = '';

    // Check for common greetings
    const normalizedMessage = message.toLowerCase().trim();
    if (greetings[normalizedMessage]) {
        addMessage(greetings[normalizedMessage], false);
        return;
    }

    try {
        const response = await fetch('https://apaskvidyabackend.onrender.com/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        // Check for unrecognized query
        if (data.response.includes("Sorry, I couldn't find an answer")) {
            const joke = await fetchJoke();
            const suggestions = getRandomSuggestions();
            const message = `${joke}<br><br><strong>Try these prompts:</strong><ul>${suggestions}</ul>`;
            addMessage(message, false);
        } else {
            addMessage(data.response, false);
        }
    } catch (error) {
        // Use sequential fallback messages
        const fallbackMessage = errorFallBacks[errorFallbackIndex % errorFallBacks.length];
        errorFallbackIndex++;
        const suggestions = getRandomSuggestions();
        const message = `${fallbackMessage}<br><br><strong>Try these prompts:</strong><ul>${suggestions}</ul>`;
        addMessage(message, false);
    }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
