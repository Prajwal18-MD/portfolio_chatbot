import os
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
import joblib

# Ensure NLTK data is present
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

# Path to resume
RESUME_PATH = os.path.join(os.path.dirname(__file__), 'static', 'Prajwal_M_D_RESUME.pdf')

# Intents and training examples
training_data = {
    'greeting': ["hi", "hello", "hey", "good morning", "good afternoon", "what's up", "sup", "heya"],
    'location': ["where are you from", "your location", "where do you live", "which city are you based", "location"],
    'education': ["your education", "where did you study", "qualification", "degree", "studied", "college"],
    'contact': ["contact", "reach you", "phone number", "call you", "message you"],
    'availability': ["when can you start", "availability", "project timeline", "how long will it take", "available"],
    'services': ["what services", "what do you offer", "capabilities", "what can you do", "services"],
    'tech_stack': ["programming languages", "frameworks", "technologies", "tech stack", "tools"],
    'projects': ["github", "portfolio", "projects", "demos", "code samples"],
    'blogs':["blogs","do you write blogs","content","do you have medium", "Any blog accounts"],
    'resume': ["resume", "cv", "overview", "pdf", "download resume", "my resume", "send resume"],
    'workflow': ["workflow", "how do you start", "process", "approach"],
    'updates': ["project updates", "track progress", "status updates", "keep updated"],
    'support': ["post-launch", "maintenance", "support", "after launch"],
    'testimonials': ["testimonials", "reviews", "feedback", "case studies"],
    'thanks': ["thanks", "thank you", "thx", "cheers"],
    'goodbye': ["bye", "goodbye", "see you later", "later"]
}

# Responses per intent
responses = {
    'greeting': [
        "Hi there! How can I help you today?",
        "Hello! Feel free to ask me anything.",
        "Hey! I'm here to assist you—ask away.",
        "Greetings! What would you like to know?",
        "Hi! Ready when you are. Ask your question."
    ],
    'location': [
        "I am from India, Karnataka, Mysuru.",
        "I'm based in Mysuru, Karnataka, India.",
        "My home is in Mysuru, India.",
        "I reside in the cultural city of Mysuru, in Karnataka, India."
    ],
    'education': [
         "I have completed B.E in Computer Science from PESCE Mandya.",
        "I studied Computer Science Engineering at PESCE Mandya.",
        "I completed my Bachelor's in Computer Science from PESCE Mandya.",
        "Graduated with a B.E in Computer Science from PESCE Mandya."
    ],
    'contact': [
        "My phone number is +91-9108402357. If unanswered, please drop your message in the contact me page below.",
        "You can contact me at +91-9108402357. If I miss your call, feel free to use the contact me page below.",
        "Reach out to me at +91-9108402357. If I’m unavailable, leave a message on the contact section below.",
        "You can give me a call at +91-9108402357 or drop a message via the contact page if I’m unavailable."
    ],
    'availability': [
        "I am available for you—just post your project details and preferred way of communication on the contact page, and I will get back to you to discuss in detail.",
        "Please share your project details and contact preferences via the contact page, and I’ll respond promptly to discuss the timeline.",
        "I’m ready to start once you provide your project information and communication method on the contact page. We can then discuss everything in detail.",
        "Share your project requirements and communication details through the contact page, and I will reach out to discuss the schedule and next steps."
    ],
    'services': [
        "I specialize in web development, deployment and integration, AI/ML development and integration, and small-scale smart contract development.",
        "My expertise includes web development, deployment and integration, AI/ML development and integration, as well as small-scale smart contracts.",
        "I offer comprehensive solutions in web development, deployment and integration, AI/ML development and integration, and small-scale smart contracts.",
        "Think of me as an AI software engineer focused on web development, deployment and integration, AI/ML projects, and small smart contract development."
    ],
    'tech_stack': [
         "I specialize in C, Python, and JavaScript, along with various frameworks and tools commonly used by AI software engineers.",
        "My expertise includes programming in C, Python, and JavaScript, plus experience with relevant frameworks and development tools.",
        "I work primarily with C, Python, and JavaScript and their associated frameworks and libraries, similar to an AI software engineer's tech stack.",
        "I am skilled in C, Python, JavaScript, and multiple frameworks and tools used in AI and software engineering."
    ],
    'projects': [
        "You can find my projects in the project section here, or check out my GitHub.",
        "Feel free to explore my work in the project section, or visit my GitHub profile.",
        "My portfolio and live demos are available in the project section, and you can also see my code on GitHub.",
        "Check out my projects and live demos in the project section, or directly on GitHub."
    ],
    'blogs':[
        "Yes, I write blogs on Medium! You can scroll down to the footer of my website to find the Medium icon — it’ll take you directly to my blog page.",
        "Absolutely! I actively publish technical blogs on Medium, covering web development, project breakdowns, and productivity tips. You can explore them through the Medium link in my site’s footer.",
        "Yes, I do blog regularly on Medium. Feel free to check out my posts — the Medium icon at the bottom of the page will take you there. Let me know what you think!"    
    ],
    'resume': [
        "Sure, here’s my resume: {}".format(RESUME_PATH),
        "Absolutely! You can download my resume from here: {}".format(RESUME_PATH),
        "Here’s a PDF overview of my work: {}".format(RESUME_PATH),
        "You can access my resume directly here: {}".format(RESUME_PATH)
    ],
    'workflow': [
        "Let's have a discussion to understand your project. Once I get a clear picture, we can plan out the budget and timeline accordingly.",
        "I typically start by understanding your requirements, then we align on the scope, budget, and timeline before development begins.",
        "First, I understand the project thoroughly through discussion, then move into planning, execution, and delivery based on your expectations.",
        "Project starts with a conversation—I get to know your goals, define the scope, and then we align on timelines and budget."
    ],
    'updates': [
        "I use Notion to share real-time progress updates—this allows clients to track the status of their project easily.",
        "Project updates are shared regularly via Notion, where clients can monitor tasks, timelines, and deliverables.",
        "I maintain a shared Notion board for each project to keep everything transparent and up-to-date.",
        "Clients get access to a Notion dashboard that reflects real-time updates on progress, milestones, and timelines."
    ],
    'support': [
       "Yes, I offer both ongoing support and maintenance after project launch.",
        "Absolutely! I provide support and maintenance services even after the deployment.",
        "Yes, I’m available for both post-launch support and future maintenance needs.",
        "Ongoing support and maintenance are part of the services I can provide after your project goes live."
    ],
    'testimonials': [
        "You can view them in the testimonials section of this website.",
        "Absolutely! Just scroll to the testimonials section to see what clients have said.",
        "Yes, check out the testimonials section here for feedback from my clients.",
        "Client reviews and case studies are available in the testimonials part of this site."
    ],
    'thanks': [
        "You’re welcome! Is there anything else I can help you with today?",
        "Happy to help! Do you have any other questions?",
        "My pleasure! Let me know if there’s anything else you need."
    ],
    'goodbye': [
        "Goodbye! Feel free to reach out anytime.",
        "See you later—thanks for stopping by!",
        "Bye for now! Don’t hesitate to get in touch again."
    ]
}

# Single fallback
fallback_response = "Sorry, I didn’t catch that. Could you rephrase? Or I might not have the answer to this—please contact me through the contact page for more details."

# Text preprocessing
def normalize(text: str):
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text.lower(), preserve_line=True)
    return ' '.join(lemmatizer.lemmatize(tok) for tok in tokens if tok.isalnum())

# Load or train model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'intent_model.pkl')
ENCODER_PATH = os.path.join(os.path.dirname(__file__), 'label_encoder.pkl')
if os.path.isfile(MODEL_PATH) and os.path.isfile(ENCODER_PATH):
    pipeline = joblib.load(MODEL_PATH)
    label_encoder = joblib.load(ENCODER_PATH)
else:
    docs, labels = [], []
    for intent, examples in training_data.items():
        for ex in examples:
            docs.append(normalize(ex))
            labels.append(intent)
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(labels)
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1,2), min_df=1)),
        ('clf', LogisticRegression(max_iter=500))
    ])
    pipeline.fit(docs, y)
    joblib.dump(pipeline, MODEL_PATH)
    joblib.dump(label_encoder, ENCODER_PATH)

# Intent prediction
def predict_intent(text: str):
    norm = normalize(text)
    probs = pipeline.predict_proba([norm])[0]
    idx = probs.argmax()
    return label_encoder.inverse_transform([idx])[0], probs[idx]

# Main response function
def get_response(user_text: str) -> str:
    text = user_text.lower()
    # 1) Keyword matching for multi-word examples
    for intent, examples in training_data.items():
        for ex in examples:
            if ' ' in ex and ex in text:
                return random.choice(responses[intent])
    # 2) ML-based intent
    intent, confidence = predict_intent(user_text)
    if confidence >= 0.12:
        return random.choice(responses[intent])
    # 3) Fallback
    return fallback_response

# CLI testing
def main():
    print("=== Ultimate Chatbot ===")
    while True:
        user = input('You: ').strip()
        if not user or user.lower() in ['exit', 'bye', 'quit']:
            print('Bot:', random.choice(responses['goodbye']))
            break
        print('Bot:', get_response(user))

if __name__ == '__main__':
    main()
