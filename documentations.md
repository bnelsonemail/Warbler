# Warbler Documentation

## Table of Contents
- [Warbler Documentation](#warbler-documentation)
  - [Table of Contents](#table-of-contents)
  - [Purpose](#purpose)
  - [File Structure](#file-structure)

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


