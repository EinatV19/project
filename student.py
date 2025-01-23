class Student (user):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self.courses = []

    def __str__(self):
        return f"Student: {self.name}, Email: {self.email}"

    def show_courses(self): #הצגת הכיתות שהתלמיד לומד
        return [course.course_name for course in self.courses]