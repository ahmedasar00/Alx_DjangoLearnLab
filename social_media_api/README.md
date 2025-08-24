# Social Media API

## Overview

This is a comprehensive RESTful API for a social media platform, built with Django and Django REST Framework. This backend service provides all the essential functionalities for a modern social network, including user authentication, profile management, a follow system, posts, comments, likes, and a real-time notification system.

---

## Features

- **User Authentication**: Secure user registration and login with token-based authentication.
- **Profile Management**: Users can create and update their profiles with a bio and a profile picture.
- **Social Graph**: A complete follow/unfollow system allowing users to connect with each other.
- **Personalized Feed**: An aggregated feed that displays the latest posts from users that the current user follows.
- **Post Management**: Full CRUD (Create, Read, Update, Delete) operations for posts.
- **Commenting System**: Users can add, view, and manage comments on posts.
- **Likes & Engagement**: Functionality for users to like and unlike posts.
- **Notification System**: Users receive notifications for new followers, likes, and comments.
- **API Enhancements**: Implements pagination for handling large datasets efficiently and filtering capabilities for posts.
- **Production Ready**: Configured for deployment to a production environment.

---

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- Pip

### Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/your-username/Alx_DjangoLearnLab.git](https://github.com/your-username/Alx_DjangoLearnLab.git)
    cd social_media_api
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required packages:**

    ```bash
    pip install django djangorestframework
    ```

    _(Note: A `requirements.txt` file is recommended for a real project)_

4.  **Apply the database migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000/`.

---

## API Documentation

All endpoints are prefixed with `/api/`. Authentication is required for most endpoints. Provide the token in the `Authorization` header as `Token <your_token>`.

### 1. Authentication

| Method | Endpoint              | Description                                |
| :----- | :-------------------- | :----------------------------------------- |
| `POST` | `/accounts/register/` | Register a new user.                       |
| `POST` | `/accounts/login/`    | Log in to receive an authentication token. |
| `GET`  | `/accounts/profile/`  | View the authenticated user's profile.     |
| `PUT`  | `/accounts/profile/`  | Update the authenticated user's profile.   |

### 2. Users & Follows

| Method | Endpoint                    | Description                                |
| :----- | :-------------------------- | :----------------------------------------- |
| `GET`  | `/users/`                   | Get a list of all users.                   |
| `GET`  | `/users/<int:pk>/`          | Retrieve a specific user's profile.        |
| `POST` | `/users/<int:pk>/follow/`   | Follow a user. (Requires authentication)   |
| `POST` | `/users/<int:pk>/unfollow/` | Unfollow a user. (Requires authentication) |

### 3. Posts & Comments

| Method   | Endpoint                    | Description                                  |
| :------- | :-------------------------- | :------------------------------------------- |
| `GET`    | `/posts/`                   | Get a list of all posts.                     |
| `POST`   | `/posts/`                   | Create a new post. (Requires authentication) |
| `GET`    | `/posts/<int:pk>/`          | Retrieve a specific post.                    |
| `PUT`    | `/posts/<int:pk>/`          | Update a post. (Owner only)                  |
| `DELETE` | `/posts/<int:pk>/`          | Delete a post. (Owner only)                  |
| `GET`    | `/posts/<int:pk>/comments/` | List all comments for a specific post.       |
| `POST`   | `/posts/<int:pk>/comments/` | Add a new comment to a post. (Requires auth) |

### 4. Likes, Feed & Notifications

| Method | Endpoint                | Description                                  |
| :----- | :---------------------- | :------------------------------------------- |
| `POST` | `/posts/<int:pk>/like/` | Like or unlike a post. (Requires auth)       |
| `GET`  | `/feed/`                | Get the personalized feed of followed users. |
| `GET`  | `/notifications/`       | Get a list of the user's notifications.      |

---

## Deployment

To deploy this API to a production environment, follow these general steps:

1.  **Production Settings:**

    - In `settings.py`, set `DEBUG = False`.
    - Configure `ALLOWED_HOSTS` with your domain name or server IP address.
    - Set up a production-grade database like PostgreSQL.

2.  **Web Server and WSGI:**

    - Use a WSGI server, such as **Gunicorn**, to run the application.
    - Use a reverse proxy, such as **Nginx**, to manage incoming HTTP requests, serve static files, and forward dynamic requests to Gunicorn.

3.  **Static & Media Files:**

    - Run `python manage.py collectstatic` to gather all static files into a single directory.
    - Configure Nginx to serve the static files and user-uploaded media files directly.

4.  **Environment Variables:**
    - Store sensitive information like `SECRET_KEY`, database credentials, and other configurations in environment variables instead of hard-coding them.

---

## Technologies Used

- **Backend:** Python, Django, Django REST Framework
- **Database:** SQLite3 (development), PostgreSQL (production recommended)
- **Authentication:** DRF Token Authentication
