import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential=cred)

db = firestore.client()

def get_users():
    return db.collection('users').get()


def get_user(user_id):
    """[summary]

    Args:
        user_id ([type]): [description]

    Returns:
        [firestore.document]: [ Firebase document instance that is converted into a dictionary]
    """
    return db.collection('users').document(user_id).get()


def get_todos(user_id):
    """[summary]

    Args:
        user_id ([type]): [description]

    Returns:
        [dict]: [User todos]
    """
    return db.collection('users').document(user_id).collection('todos').get()

def user_put(user_data):
    """[Function to load new data into firestore database]

    Args:
        user_data ([UserData]): [Instance of UserData - (username, password)]
    """
    
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({'password': user_data.password})
    
def todo_put(user_id, description):
    todos_collection_ref = db.collection('users').document(user_id).collection('todos')
    todos_collection_ref.add({'description':description, 'done':False})

def delete_todo(user_id, todo_id):
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.delete()
    # todo_ref = db.collection('users').document(user_id).collection('todos').document(todo_id)

def update_todo(user_id, todo_id, done):
    done = bool(done)
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.update({'done': not done})

def _get_todo_ref(user_id, todo_id):
    return db.document(f'users/{user_id}/todos/{todo_id}')