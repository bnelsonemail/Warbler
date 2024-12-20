# Warbler Documentation

## Table of Contents
- [Warbler Documentation](#warbler-documentation)
  - [Table of Contents](#table-of-contents)
  - [Purpose](#purpose)
  - [File Structure](#file-structure)
  - [Removed and Updated Content](#removed-and-updated-content)
    - [Authentication](#authentication)
    - [Models.py](#modelspy)
      - [Users Class](#users-class)
    - [Routes](#routes)
      - [auth/utils.py](#authutilspy)
      - [messages/routes.py](#messagesroutespy)
      - [users/routes.py](#usersroutespy)
      - [app/routes.py](#approutespy)
      - [app/models.py](#appmodelspy)
    - [Seed](#seed)
    - [app/__init__.py](#appinitpy)
    - [Forms.py](#formspy)

## Purpose

The purpose of the documentation file is to describe a high level documentation of the revisions made to the Warbler Application

## File Structure

- **Provided File Structure -** Was not very well organized.
  - App.py had all routes in it, ie:  messaging routes, auth routes, general use routes, error handling, user routes, and homepage routes.  
  - This is poor organization and will complicate the app as it is scaled.
  - The app.py file also contained all the config files and database connections

- **Revisions to Structure -** The revised structure follows Flask Standard Practices
  - See structure.md for detailed structure.
  - App.py had routes relocated throughout the app.
    - Routes.py in app folder
    - Routes.py in auth folder
  - Test folder to contain all the test files
  - run.py in the root directory to start the application.
  - app.py to direct the app to the __init__.py to create_app.
  - use of migrations to build and maintain the database

- **Blueprints -** Blueprints were added to the application
  - Blueprints are a Flask feature that helps modularize and organize the application. They allow to define routes, error handlers, and other app logic in separate components, rather than putting everything in a single routes.py file. This is especially useful for larger applications.

    1. Modular Code Organization:
      - With blueprints, you can separate different parts of your application into distinct modules (e.g., auth, users, messages), each with its own set of routes and logic.
      - This makes the codebase easier to read, maintain, and scale as new features are added.

    2. Reusability:
      - Blueprints can be reused across different Flask applications. For example, an auth blueprint managing login/logout functionality could be shared between multiple projects.

    3. Easier Collaboration:
      - In a team setting, blueprints allow developers to work on different components of the app independently without creating merge conflicts in a single routes.py file.

    4. Scalability:
      - As your app grows, a single routes.py file can become unwieldy. Blueprints provide a natural way to scale the routing logic.

    5. Improved Testing:
      - Blueprints allow for isolated testing of specific modules, making it easier to write tests for only the auth or messages routes without interfering with other parts of the app.

- **Authentication -** the "auth" folder is used for the logic and templates for authentication.  The following files will be used:
  - **__init__.py:** This is the file that makes the folders act like modules
  - **utils.py:** This file should contain helper functions that are not tied to a specific model or HTTP route but are reusable across the authentication module.  Any reusable utility functions for authentication or session management will go in this file.
  - **routes.py:** This file should focus on handling HTTP requests and responses. It interacts with forms, leverages model methods, and uses Flask-Login for session management.
  - **templates:** After many iterations and debugging, it was determined that Flask was not willing to look in the proper file folder for templates.  Therefore the templates for auth were moved to app/templates/auth.

## Removed and Updated Content

### Authentication
  - Original Auth code was placed in the wrong location.  
  - The original code was not very robust.  
  - Removing the original code can be replaced with Flask-Login's built-in functions and creates less custom code.

### Models.py
  #### Users Class
    - Optimized Relationships: Improved is_followed_by and is_following methods with database queries for scalability.
    - Simplified Password Logic: Moved hashing to set_password for consistency.
    - Error Logging: Added optional logging for failed authentication attempts.
    - Improved Authentication: Suggested an alternative for email-based login.
    - Optimized Relationship Query: The is_followed_by and is_following were updated to use efficient database queries for better scalability.
  
### Routes
  #### auth/utils.py
    - Added Type Hints: Improved code readability by explicitly defining the types of function arguments and return values.
    - Optimized Queries: Replaced .first() with exists() for better performance in large datasets.
    - Preserved Functionality: The logic and purpose of the functions remain unchanged while improving efficiency and clarity.

  #### messages/routes.py
    - Added Type Hints: Clarified the return type of each route. 
    - Refactored Ownership Check: Encapsulated the ownership check for deletion into a helper function for reusability. 
    - Improved Flash Messages: Flash messages now include contextual details (e.g., part of the message text). 
    - Added Logging: Debug and warning logs provide better traceability for key actions. 
    - Preserved Functionality: Core logic remains unchanged, ensuring that the app continues to function as expected.

  #### users/routes.py
    - Added type hints for improved readability.
    - Introduced pagination to list_users and users_show for better scalability.
    - Improved logging for follower actions and user deletion.
    - Simplified flash messages for clarity.

  #### app/routes.py
    - Removed Unused Imports: Cleaned up imports to include only the required modules and classes. 
    - Added Type Hints: Clarified the return types for all functions.
    - Improved Error Handling: Handled potential database errors when fetching messages for authenticated users.
    - Added Logging: Logged homepage access and database errors for better traceability.
    - Configurable Caching: Introduced a configuration option to enable or disable caching, making the app more adaptable to production and development environments.
    - Removed logged in user from app/routes and placed as app.before_request decorator function inside create_app

  #### app/models.py
    - Added Type Hints for improved readability.
    - Optimized Methods for checking followers and following relationships.
    - Enhanced __repr__ Methods for all models.
    - Refined signup Logic by centralizing db.session.commit().
    - Validated Input in the signup method to avoid invalid user creation.
    - Removed unique=True constraint from Likes.message_id to allow multiple likes for the same message.

### Seed
  - Encapsulated Logic: Broke the script into functions for better reusability and readability. 
  - Added Logging: Included logs to track the progress and success of each step. 
  - Introduced Error Handling: Added try-except blocks to ensure graceful handling of errors during seeding.
  - Made File Paths Configurable: Allowed file paths to be set via environment variables for flexibility.
  - Validated Input Data: Checked if files exist and are valid CSVs before processing.

### app/__init__.py
  - Refactored Configuration Logic: Extracted configuration loading into configure_app.
  - Moved Error Handlers: Centralized error handler definitions in register_error_handlers.
  - Added Debug Conditional for Route Printing: Restricted route printing to the development environment.
  - Simplified load_user: Used the existing session without explicit context management.
  - Improved Code Readability: Organized the file into logical sections for easier navigation.

### Forms.py
  - Capitalized Field Labels for consistency.
  - Added Placeholder Text to improve user experience.
  - Added a UserProfileForm to support profile editing.
  - Enhanced Validators:
    - Added Length constraints to fields like text and bio.
    - Made PasswordField consistent across forms.