# Crunch-

## Overview

Crunch- is a dynamic blog posting website designed to provide a seamless platform for users to share and explore content. This project enables users to create, edit, and manage blog posts, as well as engage with the community through comments and likes. With a modern and responsive design, Crunch- offers an enjoyable and interactive experience for both authors and readers.

## Features

- **User Registration and Authentication**: Secure user registration and login functionality.
- **Blog Creation and Management**: Create, edit, and delete blog posts with ease.
- **Rich Text Editor**: Compose blog posts with a user-friendly rich text editor.
- **Commenting System**: Engage with posts through comments.
- **Likes and Reactions**: Like and react to blog posts.
- **Categories and Tags**: Organize content with categories and tags for better discoverability.
- **Search Functionality**: Find posts quickly using the search feature.
- **Responsive Design**: Fully responsive design that works seamlessly across different devices.
- **Intuitive UI**: Clean and easy-to-use interface powered by modern front-end technologies.

## Tech Stack

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite (development), PostgreSQL (production)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Prakash5209/Crunch-.git
    cd Crunch-
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    python manage.py migrate
    ```

5. Run the development server:
    ```bash
    python manage.py runserver
    ```

6. Open your browser and navigate to `http://127.0.0.1:8000/` to see the application in action.

## Usage

- Register a new account or log in with existing credentials.
- Create new blog posts using the rich text editor.
- Edit or delete existing posts.
- Browse and read posts from other users.
- Comment on and like posts to engage with the community.

Thank you for checking out Crunch-! Happy blogging!
