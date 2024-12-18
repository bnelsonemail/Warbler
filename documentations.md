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