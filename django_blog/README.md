# Advanced Django Blog Platform

This repository contains the source code for a full-featured blogging platform built with Python and the Django Web Framework. The application supports multi-user authentication, complete content management, interactive commenting, and advanced discovery features like tagging and full-text search.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation Guide](#installation-guide)
- [Usage](#usage)
- [Author](#author)

---

## Features

The platform is equipped with a range of functionalities designed for a seamless content creation and consumption experience.

### User Authentication & Profile Management

- **User Registration:** A secure registration system for new users requiring a username, email, and password.
- **Session Management:** Robust login and logout capabilities using Django's session authentication.
- **Profile Management:** Registered users can view and update their profile details, such as their email address.
- **Permission System:** Content creation and modification are restricted to authenticated users. Authors can only edit or delete their own content.

### Content Management (CRUD)

- **Create, Read, Update, Delete (CRUD) Posts:** A complete set of class-based views for managing blog posts.
- **Dynamic Content Creation:** Authors can create posts with titles, rich text content, and associate them with multiple tags.

### Interactive Functionality

- **Commenting System:** Users can post, edit, and delete their own comments on articles to foster discussion.
- **Nested Comments:** The system supports threaded comments for organized conversations.

### Content Discovery

- **Tagging System:** Posts are categorized with tags, allowing users to browse content by topic.
- **Filter by Tag:** A dedicated view to display all posts associated with a specific tag.
- **Search Functionality:** A search engine to find posts based on keywords in the title, content, or associated tags.

---

## Technology Stack

- **Backend:** Python, Django
- **Database:** MySQL
- **Tagging:** `django-taggit`
- **Frontend:** HTML, CSS, JavaScript

---

## Project Structure

The project adheres to a standard Django application structure to ensure maintainability and scalability.
