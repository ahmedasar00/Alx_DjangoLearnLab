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

1. Clone the repository
