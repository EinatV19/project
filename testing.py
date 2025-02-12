from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["classroom"]
collection = db["courses"]

# # Find the document
# query = {"name": "Mathematics 101", "subject": "Mathematics", "teacher_mail": "q"}
#
# # Task to add
# task1 = {"task_name": "task1", "due_date": "010205", "text": "blabla"}
# task2 = {"task_name": "task2", "due_date": "012225", "text": "blibli"}

# # Push tasks to the document
# collection.update_one(query, {"$push": {"tasks": task1}})
# collection.update_one(query, {"$push": {"tasks": task2}})



# Query to find the correct document
query = {"name": "Mathematics 101", "subject": "Mathematics", "teacher_mail": "q", "tasks.task_name": "task1"}

# Student data
student1 = {"student_mail": "stusss@stu.com", "grade": "100"}
student2 = {"student_mail": "stuasa@stu.com", "grade": "80"}
student3 = {"student_mail": "cdsfstu@stu.com", "grade": "100"}
# Update: Add student to the correct task
collection.update_one(
    query,
    {"$push": {"tasks.$.students": student1}}
)
collection.update_one(
    query,
    {"$push": {"tasks.$.students": student2}}
)
collection.update_one(
    query,
    {"$push": {"tasks.$.students": student3}}
)



