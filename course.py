class Course:
    def __init__(self, course_id, course_name, teacher):
        self.course_id = course_id  # מזהה ייחודי של הקורס
        self.course_name = course_name  # שם הקורס
        self.teacher = teacher  # המורה המלמד את הקורס
        self.students = []  # רשימת תלמידים רשומים לקורס

    def add_student(self, student):
        """הוספת תלמיד לקורס"""
        self.students.append(student)

    def __str__(self):
        return f"Course: {self.course_name}, Teacher: {self.teacher.name}"