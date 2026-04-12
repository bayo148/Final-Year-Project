> Final Year Project | BSc Computer Science – University of Essex – E-commerce based AI chatbot

**Leaf** is a web-based e-commerce assistant that helps users find and compare products through a natural chat interface. It simulates an AI shopping advisor using OpenAI's GPT models, with responses tailored to each user's unique shopping style.

## How It Works

1. **User Onboarding**
   New users register and take a quick **persona quiz**. Based on their answers, they are classified as one of five shopper types:
   - Budget Buyer
   - Luxury Seeker
   - Eco-Conscious
   - Tech Enthusiast
   - Balanced Shopper

2. **Chat-Based Product Help**
   After registration, users interact with the chat interface. They describe what they're looking for (e.g. "I need a laptop for £1000") and Leaf responds with:
   - Follow-up questions to understand what they need
   - A shortlist of product options with names and estimated prices
   - Final recommendation and next steps

3. **Streaming Response Engine**
   Leaf uses OpenAI's streaming chat completions API to deliver responses in real-time.

4. **Conversation History**
   Every conversation is saved under the user's account. Users can revisit, continue, or delete past chats via the sidebar menu.

5. **Profile & Persona Management**
   Users can view and update their profile information. Their persona (e.g., "Tech Enthusiast") is shown on their profile and used to tailor responses. It can also be reset.

6. **Per-Session Message Limit**
   To prevent abuse, each user is limited to 20 messages per login session. Logging out and back in resets the counter. Staff users are exempt.

7. **Admin Management**
   A built-in Django admin panel allows full control over users, messages, and conversations.

## Personas
- **Budget Buyer** – always looking for a deal
- **Luxury Seeker** – wants the most premium products
- **Eco-Conscious** – seeks environmentally friendly options
- **Tech Enthusiast** – interested in the cutting edge
- **Balanced Shopper** – a mix of practicality, value, and quality

---

## Stack

- **Framework**: Django 5.2
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL in production (via `dj-database-url`), SQLite in local development
- **LLM**: OpenAI API (chat completions with streaming)
- **Static Files**: WhiteNoise
- **WSGI Server**: Gunicorn
- **Environment**: `python-dotenv`
- **Deployment**: Railway

## Structure

```text
Final-Year-Project/
├── core/                       # Django app
│   ├── models.py               # UserProfile, Conversation, ChatMessage
│   ├── views.py                # Auth, chat, persona quiz, profile
│   ├── forms.py                # Custom forms
│   ├── templates/core/         # HTML templates
│   └── static/core/            # theme.css + logo
├── ecommerce_assistant/        # Project settings & URLs
├── staticfiles/                # Collected static assets (served by WhiteNoise)
├── railway.toml                # Railway deployment config
├── manage.py
└── requirements.txt
```

## Setup Instructions

```bash
# 1. Clone the repo
git clone https://github.com/bayo148/Final-Year-Project.git
cd Final-Year-Project

# 2. Create a virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
# Create a .env file in the project root with:
#   SECRET_KEY=your-django-secret-key
#   DEBUG=True
#   OPENAI_API_KEY=your-openai-api-key
#
# Get an OpenAI key from https://platform.openai.com/api-keys

# 5. Run migrations
python manage.py migrate

# 6. Start the server
python manage.py runserver

# 7. For testing
python manage.py test core
```

## Deployment (Railway)

The project is configured for one-click deployment to Railway via `railway.toml`:
- `collectstatic` runs during the build phase
- `migrate` runs as the release command
- Gunicorn serves the application

Required Railway environment variables:
- `SECRET_KEY`
- `OPENAI_API_KEY`
- `DATABASE_URL` (auto-provided by Railway's Postgres plugin)
