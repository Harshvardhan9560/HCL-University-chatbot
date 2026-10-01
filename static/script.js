
const input = document.getElementById("message-input");
const chatBox = document.getElementById("chat-box");
const recentQuestions = document.getElementById("recent-questions");


// ============================================
// SEND MESSAGE
// ============================================

async function sendMessage() {

    const message = input.value.trim();

    if (message === "") {
        return;
    }

    addMessage(message, "user");

    input.value = "";

    saveRecentQuestion(message);

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });


        const data = await response.json();


        if (data.response) {

            addMessage(
                data.response,
                "bot"
            );

        } else if (data.error) {

            addMessage(
                data.error,
                "bot"
            );

        }

    } catch (error) {

        console.error(error);

        addMessage(
            "Sorry, something went wrong. Please try again.",
            "bot"
        );

    }

}


// ============================================
// ASK SUGGESTION QUESTION
// ============================================

function askQuestion(question) {

    input.value = question;

    sendMessage();

}


// ============================================
// ADD MESSAGE TO CHAT
// ============================================

function addMessage(message, type) {

    const messageDiv = document.createElement("div");

    messageDiv.classList.add(
        "message",
        type === "user"
            ? "user-message"
            : "bot-message"
    );


    const contentDiv = document.createElement("div");

    contentDiv.classList.add(
        "message-content"
    );

    contentDiv.textContent = message;


    messageDiv.appendChild(
        contentDiv
    );


    chatBox.appendChild(
        messageDiv
    );


    chatBox.scrollTop =
        chatBox.scrollHeight;

}


// ============================================
// SAVE RECENT QUESTION
// ============================================

function saveRecentQuestion(question) {

    let questions =
        JSON.parse(
            localStorage.getItem(
                "recentQuestions"
            )
        ) || [];


    // Remove duplicate
    questions =
        questions.filter(
            q => q !== question
        );


    // Add latest question first
    questions.unshift(question);


    // Keep only latest 5
    questions =
        questions.slice(0, 5);


    localStorage.setItem(
        "recentQuestions",
        JSON.stringify(questions)
    );


    displayRecentQuestions();

}


// ============================================
// DISPLAY RECENT QUESTIONS
// ============================================

function displayRecentQuestions() {

    let questions =
        JSON.parse(
            localStorage.getItem(
                "recentQuestions"
            )
        ) || [];


    recentQuestions.innerHTML = "";


    if (questions.length === 0) {

        recentQuestions.innerHTML =
            '<p class="no-recent">No recent questions</p>';

        return;
    }


    questions.forEach(
        function(question) {

            const button =
                document.createElement("button");


            button.textContent =
                question;


            button.onclick =
                function() {

                    askQuestion(question);

                };


            recentQuestions.appendChild(
                button
            );

        }
    );

}


// ============================================
// ENTER KEY TO SEND
// ============================================

input.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            sendMessage();

        }

    }
);


// ============================================
// LOAD RECENT QUESTIONS
// ============================================

displayRecentQuestions();

function toggleTheme() {
    document.body.classList.toggle("dark-mode");

    const button = document.getElementById("theme-toggle");

    if (document.body.classList.contains("dark-mode")) {
        button.textContent = "☀️";
    } else {
        button.textContent = "🌙";
    }
}