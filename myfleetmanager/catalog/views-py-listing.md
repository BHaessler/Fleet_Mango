## Function-Based Views
1. Home Page
- No specific permissions needed as it is accessible to all users.

2. Owner Success View
- No specific permissions needed as it is accessible to all users.

3. Login View
- No specific permissions needed as it is accessible to all users.

4. Register View
- No specific permissions needed as it is accessible to all users.

5. Admin Dashboard
- Uses the @user_passes_test(is_admin) decorator.

6. User List
- Uses the @user_passes_test(is_admin) decorator.

7. Add User
- Uses the @user_passes_test(is_admin) decorator.

8. Edit User
- Uses the @user_passes_test(is_admin) decorator.

9. Delete User
- Uses the @user_passes_test(is_admin) decorator.

10. User Detail
- Uses the @user_passes_test(is_admin) decorator.

11. Mechanic Dashboard
- Uses the @user_passes_test(is_mechanic) decorator.

12. Customer Dashboard
- Uses the @user_passes_test(is_customer) decorator.

13. Edit Car Instance
- Uses a combined permission check for customers, admins, and mechanics.

14. Edit Footer Content
- Uses the @user_passes_test(is_admin) decorator.

15. Feedback View
- Uses the @user_passes_test(is_customer) decorator.

16. Feedback Success View
- No specific permissions needed as it is accessible to all users.

17. Delete Feedback
- Uses the @user_passes_test(is_admin) decorator.

18. Resolve Feedback
- Uses the @user_passes_test(is_admin) decorator.

19. Feedback List View
- Uses the @user_passes_test(is_admin) decorator.

## Class-Based Views
1. Car List View
- Uses the @user_passes_test(is_admin) decorator.

2. Car Detail View
- Restricts views to only owners of their cars, however admins and mechanics
can see all the cars and all their details

3. Owner List View
- Uses UserPassesTestMixin and test_func for admin checks.

4. Owner Detail View
- No specific permissions needed; accessible to all users.

5. Owner Create View
- Use @user_passes_test(is_admin) or AdminRequiredMixin.

6. Owner Edit View
- Uses UserPassesTestMixin for permissions.

7. Customer Car List View
- Uses CustomerRequiredMixin to restrict access.