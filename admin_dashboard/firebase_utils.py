import firebase_admin
from firebase_admin import credentials, firestore
import datetime

def get_db():
    if not firebase_admin._apps:
        try:
            import os
            key_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'serviceAccountKey.json')
            if os.path.exists(key_path):
                print("Using local serviceAccountKey.json for Firebase Admin")
                cred = credentials.Certificate(key_path)
            else:
                cred = credentials.ApplicationDefault()
                
            firebase_admin.initialize_app(cred, {
                'projectId': 'testapphack',
            })
        except Exception as e:
            try:
                firebase_admin.initialize_app(options={'projectId': 'testapphack'})
            except Exception as inner_e:
                print(f"Fallback initialization failed: {inner_e}")

    try:
        db = firestore.client()
        return db
    except Exception as e:
        print(f"Error getting Firestore client: {e}")
        return None

def get_geofences():
    db = get_db()
    if not db:
        return []
    
    try:
        geofences_ref = db.collection('geofences')
        docs = geofences_ref.stream()
        
        geofences = []
        for doc in docs:
            gf_data = doc.to_dict()
            gf_data['id'] = doc.id
            geofences.append(gf_data)
            
        return geofences
    except Exception as e:
        print(f"Error reading geofences: {e}")
        return []

def get_activities():
    db = get_db()
    if not db:
        return []
        
    try:
        activities_ref = db.collection('activities').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(10)
        docs = activities_ref.stream()
        
        activities = []
        for doc in docs:
            activities.append(doc.to_dict())
            
        return activities
    except Exception as e:
        return []

def add_activity(message, icon="🔘"):
    db = get_db()
    if not db:
        return False
        
    try:
        activity_data = {
            'message': message,
            'icon': icon,
            'time_ago': 'JUST NOW',
            'timestamp': datetime.datetime.now(datetime.timezone.utc)
        }
        db.collection('activities').add(activity_data)
        return True
    except Exception as e:
        return False

# NEW: Fetch Feedbacks from Firebase
def get_feedbacks():
    db = get_db()
    if not db:
        return []
        
    try:
        # Order by timestamp if you have index, otherwise just stream
        feedbacks_ref = db.collection('feedbacks').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(50)
        docs = feedbacks_ref.stream()
        
        feedbacks = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            
            # Format timestamp nicely if it exists
            if 'timestamp' in data and data['timestamp']:
                 # Handle firestore naive timestamp vs aware datetime
                 try:
                     dt = data['timestamp']
                     data['formatted_time'] = dt.strftime("%Y-%m-%d %H:%M")
                 except Exception:
                     data['formatted_time'] = "Unknown Time"
            else:
                 data['formatted_time'] = "Just Now"

            feedbacks.append(data)
            
        return feedbacks
    except Exception as e:
        # Fallback if the descending index isn't created in firestore yet
        print(f"Error fetching ordered feedbacks (might need index): {e}. Fetching unordered...")
        try:
             docs = db.collection('feedbacks').stream()
             return [doc.to_dict() for doc in docs]
        except Exception as inner_e:
             print(f"Total failure getting feedbacks: {inner_e}")
             return []
