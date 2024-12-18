/warbler
│
├── app/                           # Main Flask application folder
│   ├── __init__.py                # Initialize the Flask app, register blueprints
│   ├── app.py                     # Entry point for running the Flask app
│   ├── forms.py                   # Flask-WTForms for handling forms
│   ├── models.py                  # Database models
│
│   ├── config/                    # Configuration settings
│   │   ├── __init__.py            # Init for config package
│   │   └── settings.py            # App-specific configurations
│
│   ├── auth/                      # Authentication-related routes and logic
│   │   ├── __init__.py            # Init for auth blueprint
│   │   ├── routes.py              # Routes for login, logout, signup
│   │   ├── utils.py               # Helper functions like `do_login`, `do_logout`
│   │   └── templates/             # Templates for auth-related pages
│   │       ├── login.html         # Login page
│   │       ├── signup.html        # Signup page
│
│   ├── users/                     # User-related routes and logic
│   │   ├── __init__.py            # Init for users blueprint
│   │   ├── routes.py              # Routes for user profiles, followers
│   │   └── templates/             # Templates for user-related pages
│   │       ├── detail.html        # User profile detail
│   │       ├── edit.html          # Edit user profile
│   │       ├── followers.html     # View followers
│   │       ├── following.html     # View following
│   │       ├── index.html         # List of users
│   │       ├── show.html          # Show user profile
│
│   ├── messages/                  # Message-related routes and logic
│   │   ├── __init__.py            # Init for messages blueprint
│   │   ├── routes.py              # Routes for creating, showing, deleting messages
│   │   └── templates/             # Templates for message-related pages
│   │       ├── new.html           # New message form
│   │       ├── show.html          # View individual message
│
│   ├── migrations/                # Database migration files
│   │   ├── __init__.py            # Init for migrations package
│   │   ├── env.py                 # Migration environment configuration
│   │   ├── script.py.mako         # Template for migration scripts
│   │   └── versions/              # Folder for migration versions
│
│   ├── static/                    # Static assets (CSS, images, etc.)
│   │   ├── favicon.ico            # Favicon for the app
│   │   ├── images/                # Folder for images
│   │   └── stylesheets/           # Folder for CSS
│   │       └── style.css          # Main stylesheet for the app
│
│   ├── templates/                 # Base templates shared across the app
│   │   ├── base.html              # Base template (extends other pages)
│   │   ├── home-anon.html         # Anonymous user home page
│   │   ├── home.html              # Logged-in user home page
│   │   ├── 404.html               # Error page for 404
│   │   ├── 500.html               # Error page for 500
│
│   ├── generator/                 # CSV generation and helper scripts
│   │   ├── __init__.py            # Init for generator package
│   │   ├── create_csvs.py         # Script to generate CSVs
│   │   ├── follows.csv            # Sample follow data
│   │   ├── helpers.py             # Utility/helper functions
│   │   ├── messages.csv           # Sample message data
│   │   └── users.csv              # Sample user data
│
│   ├── test/                      # Unit tests for models and views
│   │   ├── __init__.py            # Init for test package
│   │   ├── test_message_model.py  # Tests for Message model
│   │   ├── test_message_views.py  # Tests for Message views
│   │   ├── test_user_model.py     # Tests for User model
│   │   └── test_user_views.py     # Tests for User views
│
├── archive/                       # Backup/archive files
│
├── .gitignore                     # Specifies files for Git to ignore
├── requirements.txt               # List of project dependencies
├── seed.py                        # Script to seed the database with initial data
├── structure.md                   # File to show the file structure of the project
├── documentation.md               # File to the changes to the project
├── .env                           # Environmental variables file
└── run.py                         # Script to run the app using create_app()
