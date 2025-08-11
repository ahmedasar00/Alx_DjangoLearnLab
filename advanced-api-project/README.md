# Book API Endpoints

## List All Books
- **URL:** `/books/`
- **Method:** GET
- **Permissions:** Public
- **Description:** Returns all books, can be filtered by `author`.

## Retrieve Single Book
- **URL:** `/books/<id>/`
- **Method:** GET
- **Permissions:** Public

## Create Book
- **URL:** `/books/create/`
- **Method:** POST
- **Permissions:** Authenticated Users Only

## Update Book
- **URL:** `/books/<id>/update/`
- **Method:** PUT/PATCH
- **Permissions:** Authenticated Users Only

## Delete Book
- **URL:** `/books/<id>/delete/`
- **Method:** DELETE
- **Permissions:** Authenticated Users Only
