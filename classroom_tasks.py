from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import json

# Step 1: Authentication Setup
SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses',
    'https://www.googleapis.com/auth/classroom.topics',
    'https://www.googleapis.com/auth/classroom.coursework.me',
    'https://www.googleapis.com/auth/classroom.coursework.students',
    'https://www.googleapis.com/auth/classroom.rosters'
]

creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('classroom', 'v1', credentials=creds)

# Load JSON Input
def load_input(file_path='input.json'):
    with open(file_path, 'r') as file:
        return json.load(file)

# Step 2: List Existing Classes
def list_classes():
    results = service.courses().list().execute()
    courses = results.get('courses', [])
    for course in courses:
        print(f"{course['id']} - {course['name']}")

# Step 3: Create or Update Class (Idempotency)
def create_or_update_class(course_data):
    existing_courses = service.courses().list().execute().get('courses', [])
    for course in existing_courses:
        if course['name'] == course_data['name']:
            print(f"Class already exists: {course['name']} (ID: {course['id']})")
            return course['id']

    course = service.courses().create(body=course_data).execute()
    print(f"Course created: {course.get('name')} (ID: {course.get('id')})")
    return course['id']

# Step 4: Create, Update, or Delete Topics (Idempotency)
def sync_topics(course_id, desired_topics):
    existing_topics = service.courses().topics().list(courseId=course_id).execute().get('topic', [])
    existing_topic_names = {topic['name']: topic for topic in existing_topics}

    topic_ids = {}
    for topic_data in desired_topics:
        name = topic_data['name']
        if name in existing_topic_names:
            print(f"Topic already exists: {name}")
            topic_ids[name] = existing_topic_names[name]['topicId']
        else:
            created_topic = service.courses().topics().create(courseId=course_id, body={'name': name}).execute()
            print(f"Created topic: {created_topic['name']}")
            topic_ids[name] = created_topic['topicId']

    # Delete topics not in desired list
    for topic in existing_topics:
        if topic['name'] not in [t['name'] for t in desired_topics]:
            service.courses().topics().delete(courseId=course_id, id=topic['topicId']).execute()
            print(f"Deleted topic: {topic['name']}")

    return topic_ids

# Step 5: Add, Update, or Delete Sub-Topics (Coursework)
def sync_coursework(course_id, topic_ids, sub_topics):
    existing_coursework = service.courses().courseWork().list(courseId=course_id).execute().get('courseWork', [])
    existing_titles = {cw['title']: cw for cw in existing_coursework}

    for sub_topic in sub_topics:
        title = sub_topic['title']
        topic_name = sub_topic['topic']
        topic_id = topic_ids.get(topic_name)

        coursework_body = {
            'title': title,
            'description': sub_topic['description'],
            'materials': [{'link': {'url': sub_topic['link']}}] if sub_topic.get('link') else [],
            'topicId': topic_id,
            'workType': 'ASSIGNMENT',
            'state': 'PUBLISHED'
        }

        if title in existing_titles:
            existing = existing_titles[title]
            # If changes detected, delete and recreate coursework
            if (existing['description'] != sub_topic['description'] or
                existing.get('materials', [{}])[0].get('link', {}).get('url', '') != sub_topic.get('link', '')):
                service.courses().courseWork().delete(courseId=course_id, id=existing['id']).execute()
                print(f"Deleted outdated coursework: {title}")
                service.courses().courseWork().create(courseId=course_id, body=coursework_body).execute()
                print(f"Recreated coursework: {title}")
            else:
                print(f"Coursework already exists and is up to date: {title}")
        else:
            service.courses().courseWork().create(courseId=course_id, body=coursework_body).execute()
            print(f"Created coursework: {title}")

    # Delete coursework not in sub_topics
    for cw in existing_coursework:
        if cw['title'] not in [st['title'] for st in sub_topics]:
            service.courses().courseWork().delete(courseId=course_id, id=cw['id']).execute()
            print(f"Deleted coursework: {cw['title']}")

# Step 6: Verify the Created Class, Topics, and Materials
def verify_class(course_id):
    print("\nVerifying Class and Topics:")
    topics = service.courses().topics().list(courseId=course_id).execute()
    for topic in topics.get('topic', []):
        print(f"Topic: {topic['name']}")

    courseworks = service.courses().courseWork().list(courseId=course_id).execute()
    for coursework in courseworks.get('courseWork', []):
        print(f"Coursework: {coursework['title']}")

# Main Execution
if __name__ == "__main__":
    data = load_input()
    list_classes()
    course_id = create_or_update_class(data['course'])
    topic_ids = sync_topics(course_id, data['topics'])
    sync_coursework(course_id, topic_ids, data['sub_topics'])
    verify_class(course_id)
