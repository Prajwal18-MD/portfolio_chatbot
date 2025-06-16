import os
import nltk
from nltk.chat.util import Chat, reflections

# If first time, uncomment to download NLTK data:
nltk.download('punkt')
nltk.download('wordnet')

# Path to your static resume file
RESUME_PATH = os.path.join(os.path.dirname(__file__), 'static', 'Prajwal_M_D_RESUME.pdf')

pairs = [
[
    r".*(hi|hello|hey|holla|yo|good (morning|afternoon|evening)|what's up|sup|heya).*",
    [
        "Hi there! How can I help you today?",
        "Hello! Feel free to ask me anything.",
        "Hey! I'm here to assist you—ask away.",
        "Greetings! What would you like to know?",
        "Hi! Ready when you are. Ask your question."
    ]
],
   
[
    r".*(where.*(you.*(from|stay|based)|location|belong)).*",
    [
        "I am from India, Karnataka, Mysuru.",
        "I'm based in Mysuru, Karnataka, India.",
        "My home is in Mysuru, India.",
        "I reside in the cultural city of Mysuru, in Karnataka, India."
    ]
],

    [
    r".*(education|study|qualification|college|school|course).*",
    [
        "I have completed B.E in Computer Science from PESCE Mandya.",
        "I studied Computer Science Engineering at PESCE Mandya.",
        "I completed my Bachelor's in Computer Science from PESCE Mandya.",
        "Graduated with a B.E in Computer Science from PESCE Mandya."
    ]
],
    [
    r".*(contact|reach|phone number|call|message|get in touch).*",
    [
        "My phone number is +91-9108402357. If unanswered, please drop your message in the contact me page below.",
        "You can contact me at +91-9108402357. If I miss your call, feel free to use the contact me page below.",
        "Reach out to me at +91-9108402357. If I’m unavailable, leave a message on the contact section below.",
        "You can give me a call at +91-9108402357 or drop a message via the contact page if I’m unavailable."
    ]
],
    [
    r".*(availability|available|project timeline|timeline|when can you start|current schedule|project duration|how long).*",
    [
        "I am available for you—just post your project details and preferred way of communication on the contact page, and I will get back to you to discuss in detail.",
        "Please share your project details and contact preferences via the contact page, and I’ll respond promptly to discuss the timeline.",
        "I’m ready to start once you provide your project information and communication method on the contact page. We can then discuss everything in detail.",
        "Share your project requirements and communication details through the contact page, and I will reach out to discuss the schedule and next steps."
    ]
],
    [
    r".*(services|offer|what do you do|capabilities|what can you (provide|offer)).*",
    [
        "I specialize in web development, deployment and integration, AI/ML development and integration, and small-scale smart contract development.",
        "My expertise includes web development, deployment and integration, AI/ML development and integration, as well as small-scale smart contracts.",
        "I offer comprehensive solutions in web development, deployment and integration, AI/ML development and integration, and small-scale smart contracts.",
        "Think of me as an AI software engineer focused on web development, deployment and integration, AI/ML projects, and small smart contract development."
    ]
],
    [
    r".*(programming languages|languages|frameworks|technologies|tools|tech stack|specialize in|expertise).*",
    [
        "I specialize in C, Python, and JavaScript, along with various frameworks and tools commonly used by AI software engineers.",
        "My expertise includes programming in C, Python, and JavaScript, plus experience with relevant frameworks and development tools.",
        "I work primarily with C, Python, and JavaScript and their associated frameworks and libraries, similar to an AI software engineer's tech stack.",
        "I am skilled in C, Python, JavaScript, and multiple frameworks and tools used in AI and software engineering."
    ]
],
    [
    r".*(github|projects|portfolio|demos|live demos|code samples|source code|link).*",
    [
        "You can find my projects in the project section here, or check out my GitHub.",
        "Feel free to explore my work in the project section, or visit my GitHub profile.",
        "My portfolio and live demos are available in the project section, and you can also see my code on GitHub.",
        "Check out my projects and live demos in the project section, or directly on GitHub."
    ]
],
    [
    r".*(resume|cv|overview|pdf).*",
    [
        "Sure, here’s my resume: {}".format(RESUME_PATH),
        "Absolutely! You can download my resume from here: {}".format(RESUME_PATH),
        "Here’s a PDF overview of my work: {}".format(RESUME_PATH),
        "You can access my resume directly here: {}".format(RESUME_PATH)
    ]
],
    [
    r".*(approach|how do you start|how do you handle|project process|start to finish|workflow).*",
    [
        "Let's have a discussion to understand your project. Once I get a clear picture, we can plan out the budget and timeline accordingly.",
        "I typically start by understanding your requirements, then we align on the scope, budget, and timeline before development begins.",
        "First, I understand the project thoroughly through discussion, then move into planning, execution, and delivery based on your expectations.",
        "Project starts with a conversation—I get to know your goals, define the scope, and then we align on timelines and budget."
    ]
],
    [
    r".*(keep.*updated|track progress|project updates|how do you update|status updates|client updates).*",
    [
        "I use Notion to share real-time progress updates—this allows clients to track the status of their project easily.",
        "Project updates are shared regularly via Notion, where clients can monitor tasks, timelines, and deliverables.",
        "I maintain a shared Notion board for each project to keep everything transparent and up-to-date.",
        "Clients get access to a Notion dashboard that reflects real-time updates on progress, milestones, and timelines."
    ]
],
    [
    r".*(support|maintenance|after launch|post[- ]launch|after delivery|ongoing help|future issues).*",
    [
        "Yes, I offer both ongoing support and maintenance after project launch.",
        "Absolutely! I provide support and maintenance services even after the deployment.",
        "Yes, I’m available for both post-launch support and future maintenance needs.",
        "Ongoing support and maintenance are part of the services I can provide after your project goes live."
    ]
],
    [
    r".*(testimonials|reviews|feedback|case studies|client experiences|customer stories).*",
    [
        "You can view them in the testimonials section of this website.",
        "Absolutely! Just scroll to the testimonials section to see what clients have said.",
        "Yes, check out the testimonials section here for feedback from my clients.",
        "Client reviews and case studies are available in the testimonials part of this site."
    ]
],
    [
    r".*(thank(s| you)|thank you|thx|cheers).*",
    [
        "You’re welcome! Is there anything else I can help you with today?",
        "Happy to help! Do you have any other questions?",
        "My pleasure! Let me know if there’s anything else you need."
    ]
],
[
    r".*(no(pe)?|nothing|that('?s)? it|bye|goodbye|see you|later).*",
    [
        "Goodbye! Feel free to reach out anytime.",
        "See you later—thanks for stopping by!",
        "Bye for now! Don’t hesitate to get in touch again."
    ]
],
[
    r"(.*)",
    [
        "Sorry, I didn’t catch that. Could you rephrase? Or I might not have the answer to this—please contact me through the contact page for more details."
    ]
]
]

# Instantiate once
_chatbot = Chat(pairs, reflections)

def get_response(text: str) -> str:
    """
    Return a single reply for the given user text.
    """
    reply = _chatbot.respond(text)
    # If NLTK returns None (no match), use a default
    return reply or "Hmm—I’m not sure how to answer that."

def main():
    print("=== NLTK Chatbot (interactive) ===")
    print("Type 'exit' or 'bye' to quit.\n")
    _chatbot.converse()

if __name__ == "__main__":
    main()
