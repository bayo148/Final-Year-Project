> Final Year Project | BSc Computer Science – University of Essex - Ecommerce based AI chatbot


**Leaf** is a web-based e-commerce assistant that helps users find and compare products through a natural chat interface. It simulates an AI shopping advisor using GPT-4o, with responses tailored to each user’s unique shopping style.

## How It Works

1. **User Onboarding**  
   New users register and take a quick **persona quiz**. Based on their answers, they are classified as one of five shopper types:
   - Budget Buyer  
   - Luxury Seeker  
   - Eco-Conscious  
   - Tech Enthusiast  
   - Balanced Shopper  


2. **Chat-Based Product Help**  
   After registration, users interact with the chat interface. They describe what they’re looking for (e.g. “I need a laptop for £1000”) and Leaf responds with:
   - Follow-up questions to understand what they need 
   - A shortlist of product options with names and estimated prices  
   - Final recommendation and next steps  


3. **Streaming Response Engine**  
   Leaf uses the GPT-4o model via OpenAI’s streaming API to deliver responses in real-time.


4. **Conversation History**  
   Every conversation is saved under a session. Users can revisit, continue, or delete past chats via the sidebar menu.


5. **Profile & Persona Management**  
   Users can view and update their profile information. Their persona (e.g., “Tech Enthusiast”) is shown on their profile and used to tailor responses. It can also be reset.


6. **Admin Management**  
   A built-in Django admin panel allows full control over users, messages, and conversations.


 Personas
- **Budget Buyer - always looking for a deal**
- **Luxury Seeker - want the most premium products**
- **Eco-Conscious - seeking environmentally friendly options**
- **Tech Enthusiast - interested in the cutting edge**
- **Balanced Shopper - perfectly balanced**

---

## Stack

- **Framework**: Django
- **Frontend**: HTML, CSS, JS
- **Database**: SQLite
- **LLM**: OpenAI API (GPT-4o)
- **Environment**: `python-dotenv`
- **Deployment**: Local



## Structure

```text
24‑25_CE301_oguntimehin_mobayonle_p/
├── core/                 # Django app with models, views, etc.
│   ├── templates/core/   # HTML templates
│   └── static/core/      # theme.css + assets
├── ecommerce_assistant/  # Project settings & URLs
├── manage.py
└── requirements.txt
```

## Setup Instructions

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/leaf-chatbot.git
cd leaf-chatbot

# 2. Create a virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
# Create a .env file in the project root and add your OpenAI API key:
# OPENAI_API_KEY=your-actual-key-here
#
# You must provide your own API key from https://platform.openai.com/api-keys
# After editing .env, make sure you SAVE the file before starting the server,
# otherwise the placeholder value will be used and the chat will not work.

# 5. Run migrations
python manage.py migrate

# 6. Start the server
python manage.py runserver

# 7. For testing
python manage.py test core


