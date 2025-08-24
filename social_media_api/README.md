# Social Media API

## Overview

This is a Social Media API built with Django and Django REST Framework.
It provides user registration, login, profile management, and token-based authentication.

## Features

- Custom user model (CustomerUserModel) with:
  - username, email, password
  - bio
  - profile_picture
  - followers (self-referential ManyToMany)
- User registration and login with token authentication
- Profile view and update for authenticated users
- API using DRF serializers and routers

## Installation

# Social Media API - Posts & Comments Functionality

## Overview

The goal of this task is to **implement core social media features** by adding **Posts** and **Comments** functionalities to the existing `social_media_api` project.  
This enables users to **create, view, update, and delete posts and comments**, providing essential interaction within the platform.

---

## Task Description

Expand the `social_media_api` project by creating functionality for users to manage posts and engage with them through comments.

This involves setting up:

- **Models**
- **Serializers**
- **Views**
- **Routes (URLs)**

---

## Implementation Steps

### Step 1: Create Post and Comment Models

- Create a new app: `posts`
- Define two models:
  - **Post**
    - `author` → ForeignKey to `User`
    - `title` → CharField
    - `content` → TextField
    - `created_at`, `updated_at` → DateTime fields
  - **Comment**
    - `post` → ForeignKey to `Post`
    - `author` → ForeignKey to `User`
    - `content`
    - `created_at`, `updated_at`
- Run migrations:
  ```bash
  python manage.py makemigrations posts
  python manage.py migrate
  ```

# Social Media API - User Follows & Feed Functionality

## Objective

The goal of this task is to **expand the social media features** by implementing:

- **User follow/unfollow functionality**
- **Aggregated feed of posts** from followed users

This enhances the social aspect of the platform, similar to popular social media networks.

---

## Task Description

Build on the existing `social_media_api` project by adding user relationships and a dynamic content feed.

Key features include:

- Managing **user follow relationships**
- Creating a **feed view** that displays posts from users that a given user follows

---

## Implementation Steps

### Step 1: Update User Model to Handle Follows

- Modify your **custom user model** (`CustomerUserModel`) to include:
  - `following` → ManyToManyField to itself, representing users that a user follows
- Run migrations to update the database:

```bash
python manage.py makemigrations accounts
python manage.py migrate
```
