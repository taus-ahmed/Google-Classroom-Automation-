import json
from classroom import create_classroom, update_classroom, get_classroom
from teacher import create_teacher, update_teacher, get_teacher
from student import create_student, update_student, get_student
from topic import create_topic, update_topic, get_topic


class Orchestrator:
    """Class to handle orchestration of Google Classroom operations."""

    def __init__(self, json_file: str):
        """Initialize with the JSON file path."""
        self.json_file = json_file
        self.classroom_data = None

    def load_from_json(self):
        """Load classroom data from the JSON file."""
        try:
            with open(self.json_file, "r") as f:
                self.classroom_data = json.load(f)

            if "classrooms" not in self.classroom_data:
                raise KeyError("Missing 'classrooms' key in JSON file")

            return self.classroom_data

        except (FileNotFoundError, json.JSONDecodeError) as e:
            return None  # Suppress print statements for cleaner test output

    def save_to_google_classroom(self):
        """Create classrooms, teachers, students, and topics in Google Classroom."""
        if not self.classroom_data:
            print("No classroom data loaded.")
            return []

        created_data = []

        for classroom in self.classroom_data["classrooms"]:
            created_class = create_classroom(
                classroom["name"],
                classroom["section"],
                classroom["description"]
            )

            classroom_id = created_class["id"]

            # Adding teachers
            created_teachers = []
            for teacher in classroom.get("teachers", []):
                created_teacher = create_teacher(teacher["name"], teacher["email"], teacher["subjects"])
                created_teachers.append(created_teacher)

            # Adding students
            created_students = []
            for student in classroom.get("students", []):
                print(f"Processing student: {student}")
                created_student = create_student(student["name"], student["email"], student["age"], student["grade"], student["courses"])
                created_students.append(created_student)

            # Adding topics
            created_topics = []
            for topic in classroom.get("topics", []):
                teacher_id = created_teachers[0]["id"] if created_teachers else None
                created_topic = create_topic(topic["name"], topic["description"], teacher_id, classroom_id)
                created_topics.append(created_topic)

            # Simulating an update
            updated_class = update_classroom(classroom_id, name="Updated " + created_class["name"])
            created_data.append({
                "classroom": updated_class,
                "teachers": created_teachers,
                "students": created_students,
                "topics": created_topics
            })

        return created_data


if __name__ == "__main__":
    classroom_file = "classroom_data.json"
    orchestrator = Orchestrator(classroom_file)

    # Load classrooms from JSON
    if orchestrator.load_from_json():
        results = orchestrator.save_to_google_classroom()

        print("Final Classroom Data:")
        for data in results:
            print(data)

# import json
# from classroom import create_classroom, update_classroom
#
#
# class Orchestrator:
#     """Class to handle orchestration of Google Classroom operations."""
#
#     def __init__(self, json_file: str):
#         """Initialize with the JSON file path."""
#         self.json_file = json_file
#         self.classroom_data = None
#
#     def load_from_json(self):
#         """Load classroom data from the JSON file."""
#         try:
#             with open(self.json_file, "r") as f:
#                 self.classroom_data = json.load(f)
#
#             if "classrooms" not in self.classroom_data:
#                 raise KeyError("Missing 'classrooms' key in JSON file")
#
#             return self.classroom_data
#
#         except (FileNotFoundError, json.JSONDecodeError) as e:
#             return None  # Suppress print statements for cleaner test output
#
#     def save_to_google_classroom(self):
#         """Create classrooms in Google Classroom and update them."""
#         if not self.classroom_data:
#             print("No classroom data loaded.")
#             return []
#
#         created_classrooms = []
#
#         for classroom in self.classroom_data["classrooms"]:
#             created_class = create_classroom(
#                 classroom["name"],
#                 classroom["section"],
#                 classroom["description"]
#             )
#
#             # Simulating an update
#             updated_class = update_classroom(int(created_class["id"]), name="Updated " + created_class["name"])
#             created_classrooms.append(updated_class)
#
#         return created_classrooms
#
#
# if __name__ == "__main__":
#     classroom_file = "classroom_data.json"
#
#     orchestrator = Orchestrator(classroom_file)
#
#     # Load classrooms from JSON
#     if orchestrator.load_from_json():
#         results = orchestrator.save_to_google_classroom()
#
#         print("Final Classroom Data:")
#         for classroom in results:
#             print(classroom)
#
# # import json
# # from classroom import create_classroom, update_classroom
# #
# # def load_json(json_file: str):
# #     """Load JSON data from a file."""
# #     with open(json_file, "r") as f:
# #         return json.load(f)
# #
# # def orchestrate_classroom_operations(json_file: str):
# #     """Load classroom data from JSON, create multiple classrooms, and update them."""
# #     classroom_data = load_json(json_file)
# #
# #     created_classrooms = []
# #
# #     # Ensure the key "classrooms" exists in the JSON file
# #     if "classrooms" not in classroom_data:
# #         raise KeyError("Missing 'classrooms' key in JSON file")
# #
# #     # Loop through each classroom entry in the JSON
# #     for classroom in classroom_data["classrooms"]:
# #         created_class = create_classroom(
# #             classroom["name"],
# #             classroom["section"],
# #             classroom["description"],
# #         )
# #
# #         # Simulating an update (change name)
# #         updated_class = update_classroom(int(created_class["id"]), name="Updated " + created_class["name"])
# #         created_classrooms.append(updated_class)
# #
# #     return created_classrooms
# #
# # if __name__ == "__main__":
# #     classroom_file = "classroom_data.json"
# #     try:
# #         results = orchestrate_classroom_operations(classroom_file)
# #         print("Final Classroom Data:")
# #         for classroom in results:
# #             print(classroom)
# #     except Exception as e:
# #         print(f"Error: {e}")
