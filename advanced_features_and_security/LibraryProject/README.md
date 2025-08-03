# Permissions and Groups Setup

This application implements custom permissions and groups to control access to the `Article` model.

## Custom Permissions

The `Article` model defines the following permissions:

- `can_view`: Can view article
- `can_create`: Can create article
- `can_edit`: Can edit article
- `can_delete`: Can delete article

Defined in `models.py` under the `Meta` class.

## Groups and Permissions

Three groups are configured in the Django admin:

- **Viewers**: Has `can_view` permission.
- **Editors**: Has `can_view`, `can_create`, and `can_edit` permissions.
- **Admins**: Has all permissions including `can_delete`.

## Views and Permission Enforcement

In `views.py`, Django's `@permission_required` decorator is used to protect views:

- `article_list`: Requires `can_view`
- `article_create`: Requires `can_create`
- `article_edit`: Requires `can_edit`
- `article_delete`: Requires `can_delete`

## Testing

Permissions are tested manually by assigning users to different groups via the Django admin interface, and verifying their access.
