# myapp/templatetags/my_filters.py

from django import template

register = template.Library()

@register.filter
def get_item(user_list, user_id):
    """Retrieve the username from the user list based on the user_id."""
    user = next((user for user in user_list if user.id == user_id), None)
    return user.username if user else "Unknown User"  # Return a default message if user is not found
