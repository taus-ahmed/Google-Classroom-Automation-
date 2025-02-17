import json

class Orchestrator:
    def __init__(self, json_file):
        self.json_file = json_file
        self.data = self.load_json()
        print("Orchestrator initialized with JSON file.")

    def load_json(self):
        """Load JSON file and return data."""
        try:
            with open(self.json_file, 'r') as file:
                print("Loading JSON file...")
                return json.load(file)
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return None

    def process_data(self):
        """Iterate through JSON data and create classes, topics, and subtopics."""
        if not self.data:
            print("No data available.")
            return

        print("Processing data...")
        for class_info in self.data.get("classes", []):
            class_name = class_info.get("name")
            subject = class_info.get("subject")
            teacher = Teacher(class_info.get("teacher"))
            classroom = Classroom(class_name, subject, teacher)
            print(f"Created Class: {class_name} ({subject}) by {teacher.name}")

            for topic_info in class_info.get("topics", []):
                topic_name = topic_info.get("name")
                topic = classroom.create_topic(topic_name)
                print(f"  Added Topic: {topic_name}")

                for subtopic_info in topic_info.get("subtopics", []):
                    subtopic_title = subtopic_info.get("title")
                    description = subtopic_info.get("description")
                    topic.add_subtopic(subtopic_title, description)
                    print(f"    Added Subtopic: {subtopic_title}")

            for student_info in class_info.get("students", []):
                student = Student(student_info.get("name"), student_info.get("id"))
                classroom.add_student(student)
                print(f"  Assigned Student: {student.name}")

class Classroom:
    def __init__(self, name, subject, teacher):
        self.name = name
        self.subject = subject
        self.teacher = teacher
        self.topics = []
        self.students = []
        print(f"Classroom created: {self.name} - {self.subject}")

    def create_topic(self, topic_name):
        topic = Topic(topic_name)
        self.topics.append(topic)
        print(f"Topic created: {topic_name}")
        return topic
    
    def add_student(self, student):
        self.students.append(student)
        print(f"Student added to class: {student.name}")

class Topic:
    def __init__(self, name):
        self.name = name
        self.subtopics = []
        print(f"Topic initialized: {self.name}")

    def add_subtopic(self, title, description):
        subtopic = SubTopic(title, description)
        self.subtopics.append(subtopic)
        print(f"Subtopic added: {title}")

class SubTopic:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        print(f"SubTopic initialized: {self.title}")

class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        print(f"User created: {self.name} - ID: {self.user_id}")

class Student(User):
    def __init__(self, name, student_id):
        super().__init__(name, student_id)
        print(f"Student created: {self.name} - ID: {student_id}")

class Teacher(User):
    def __init__(self, name):
        super().__init__(name, None)
        print(f"Teacher created: {self.name}")

class Assignment:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        print(f"Assignment created: {self.title}")

    def generate_pdf(self):
        print(f"Generating PDF for {self.title}")
        return f"PDF for {self.title} generated."

# Example Usage
if __name__ == "__main__":
    print("Starting Orchestrator...")
    orchestrator = Orchestrator("input.json")
    orchestrator.process_data()
    print("Processing complete.")
