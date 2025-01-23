class UserManager:
    def __init__(self):
        self.users = []  # רשימה של כל המשתמשים
        self.courses = []  # רשימה של כל הקורסים

    def add_user(self, user):
        """הוספת משתמש חדש"""
        self.users.append(user)

    def add_course(self, course):
        """הוספת קורס חדש"""
        self.courses.append(course)

    def get_user_by_email(self, email):
        """חיפוש משתמש לפי אימייל"""
        for user in self.users:
            if user.email == email:
                return user
        return None

    def login(self, email):
        """התחברות למערכת והצגת הכיתות של המשתמש"""
        user = self.get_user_by_email(email)
        if user:
            print(f"Hello, {user.name}!")
            # הצגת הכיתות של המשתמש (תלמיד או מורה)
            if isinstance(user, Student):
                print(f"Your enrolled courses: {', '.join(user.show_courses())}")
            elif isinstance(user, Teacher):
                print(f"You teach the following courses: {', '.join(user.show_courses())}")
        else:
            print("User not found.")