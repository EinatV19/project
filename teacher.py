class Teacher (user):
    def __init__(self, user_id, name, email, subjects):
        super().__init__(user_id, name, email)
        self.subjects = subjects  # רשימת המקצועות שהמורה מלמד
        self.courses = []  # רשימה של כיתות שהמורה מלמד

    def __str__(self): #המרת האובייקט למחרוזרת (מסדר את מאפייני המחרוזת)
        return f"Teacher: {self.name}, Email: {self.email}"

    def show_courses(self): #הצגת הכיתות שהמורה מלמד
        return [course.course_name for course in self.courses]