import tkinter as tk


def open_courses_window(courses_data):
    # Close the login window
    login_window.destroy()  # Close the login window (this assumes the login window is named login_window)

    # Create a new window for courses
    courses_window = tk.Tk()
    courses_window.title("בחר כיתה")

    # Set the window size (optional, you can customize as needed)
    courses_window.geometry("600x400")

    # Add a label for the courses window
    label_courses = tk.Label(courses_window, text="בחר כיתה", font=("Arial", 20))
    label_courses.pack(pady=20)

    # Retrieve courses from the dictionary
    courses = courses_data.get('courses', [])

    # Create a button for each course in the dictionary
    for course in courses:
        course_name = course.get('name', 'Unknown Course')  # Use 'Unknown Course' if name is missing
        btn_course = tk.Button(courses_window, text=course_name, font=("Arial", 16), width=20, height=2,
                               command=lambda c=course: CourseWindow(None, c))  # Create a new window for the course
        btn_course.pack(pady=10)

    # Add a "Create New Course" button to open a new course creation window
    def create_new_course():
        print("Creating a new course...")  # You can replace this with the actual function to create a new course
        # You might want to call a separate function here for course creation
        pass  # Replace with actual logic for creating a new course

    btn_create_new_course = tk.Button(courses_window, text="Create New Course", font=("Arial", 16), width=20, height=2,
                                      command=create_new_course)
    btn_create_new_course.pack(pady=10)

    # Run the courses window event loop
    courses_window.mainloop()


# Example usage with a dictionary of courses
courses_data = {
    'status': 'success',
    'courses': [
        {'name': 'Mathematics 101', 'subject': 'Mathematics', 'teacher_mail': 'q'},
        {'name': 'Physics 101', 'subject': 'Physics', 'teacher_mail': 'q'}
    ]
}

# Open the courses window with the example data
open_courses_window(courses_data)
