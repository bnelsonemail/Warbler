

/warbler
│
├── app/                           # Main Flask application folder
│   ├── __init__.py                # (Optional) Initialize the Flask app
│   ├── app.py                     # Entry point for running the Flask app
│   ├── forms.py                   # Flask-WTForms for handling forms
│   ├── models.py                  # Database models
│
│   ├── config/                    # Configuration settings
│   │   └── settings.py            # App-specific configurations
│
│   ├── generator/                 # CSV generation and helper scripts
│   │   ├── create_csvs.py         # Script to generate CSVs
│   │   ├── follows.csv            # Sample follow data
│   │   ├── helpers.py             # Utility/helper functions
│   │   ├── messages.csv           # Sample message data
│   │   └── users.csv              # Sample user data
│
│   ├── static/                    # Static assets (CSS, images, etc.)
│   │   ├── favicon.ico            # Favicon for the app
│   │   ├── images/                # Folder for images
│   │   └── stylesheets/           # Folder for CSS
│   │       └── style.css          # Main stylesheet for the app
│
│   ├── templates/                 # Jinja2 templates for rendering HTML
│   │   ├── base.html              # Base template (extends other pages)
│   │   ├── home-anon.html         # Anonymous user home page
│   │   ├── home.html              # Logged-in user home page
│   │
│   │   ├── messages/              # Message-related templates
│   │   │   ├── new.html           # New message form
│   │   │   └── show.html          # View individual message
│   │
│   │   └── users/                 # User-related templates
│   │       ├── detail.html        # User profile detail
│   │       ├── edit.html          # Edit user profile
│   │       ├── followers.html     # View followers
│   │       ├── following.html     # View following
│   │       ├── index.html         # List of users
│   │       ├── login.html         # Login page
│   │       ├── show.html          # Show user profile
│   │       └── signup.html        # Signup page
│
│   ├── test/                      # Unit tests for models and views
│   │   ├── test_message_model.py  # Tests for Message model
│   │   ├── test_message_views.py  # Tests for Message views
│   │   ├── test_user_model.py     # Tests for User model
│   │   └── test_user_views.py     # Tests for User views
│
├── archive/                       # Backup/archive files
│
├── .gitignore                     # Specifies files for Git to ignore
├── requirements.txt               # List of project dependencies
└── seed.py                        # Script to seed the database with initial data
