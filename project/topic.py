import uuid

# In-memory storage for topics
topic_store = {}


def validate_topic(name, description):
    """Validates topic details before creation or update."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Topic name must be a non-empty string.")
    if not isinstance(description, str) or not description.strip():
        raise ValueError("Topic description must be a non-empty string.")


def create_topic(name, description, teacher_id, classroom_id):
    """
    Creates a new topic with a unique ID.

    :param name: Topic name
    :param description: Topic description
    :param teacher_id: ID of the teacher who created the topic
    :param classroom_id: ID of the classroom associated with the topic
    :return: Created topic dictionary
    """
    validate_topic(name, description)

    topic_id = str(uuid.uuid4())
    topic = {
        "id": topic_id,
        "name": name,
        "description": description,
        "teacher_id": teacher_id,
        "classroom_id": classroom_id
    }
    topic_store[topic_id] = topic
    return topic


def get_topic(topic_id):
    """
    Retrieves a topic by its ID.

    :param topic_id: The topic ID
    :return: Topic dictionary
    :raises KeyError: If topic is not found
    """
    if topic_id not in topic_store:
        raise KeyError("Topic not found.")
    return topic_store[topic_id]


def update_topic(topic_id, name=None, description=None):
    """
    Updates a topic's details.

    :param topic_id: The topic ID
    :param name: New name (optional)
    :param description: New description (optional)
    :return: Updated topic dictionary
    :raises KeyError: If topic is not found
    """
    if topic_id not in topic_store:
        raise KeyError("Topic not found.")

    topic = topic_store[topic_id]

    if name is not None:
        validate_topic(name, topic["description"])
        topic["name"] = name

    if description is not None:
        validate_topic(topic["name"], description)
        topic["description"] = description

    return topic
