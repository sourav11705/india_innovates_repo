import firebase_admin
from firebase_admin import credentials, firestore
import datetime

def seed_database():
    print("Initializing Firebase...")
    try:
        import os
        key_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'serviceAccountKey.json')
        if os.path.exists(key_path):
            print("Using local serviceAccountKey.json")
            cred = credentials.Certificate(key_path)
        else:
            cred = credentials.ApplicationDefault()
            
        firebase_admin.initialize_app(cred, {
            'projectId': 'testapphack',
        })
    except ValueError:
        pass
    except Exception as e:
         print(f"Fallback init: {e}")
         firebase_admin.initialize_app(options={'projectId': 'testapphack'})

    db = firestore.client()
    
    print("Seeding Geofences from Master Dataset...")
    geofences = [
        # HOSPITALS (Red)
        { "id": "GF-H-1", "title": "AIIMS New Delhi", "type": "Hospital", "coords": [28.5672, 77.2100], "radius": 0.5, "color": "#ef4444", "message": "Public Health Zone: Strict Silence required. No honking." },
        { "id": "GF-H-2", "title": "Safdarjung Hospital", "type": "Hospital", "coords": [28.5663, 77.2075], "radius": 0.5, "color": "#ef4444", "message": "Public Health Zone: Strict Silence required. No honking." },
        { "id": "GF-H-3", "title": "Ram Manohar Lohia (RML)", "type": "Hospital", "coords": [28.6253, 77.2013], "radius": 0.5, "color": "#ef4444", "message": "Public Health Zone: Strict Silence required. No honking." },
        { "id": "GF-H-4", "title": "Lok Nayak Hospital (LNJP)", "type": "Hospital", "coords": [28.6366, 77.2343], "radius": 0.5, "color": "#ef4444", "message": "Public Health Zone: Strict Silence required. No honking." },
        { "id": "GF-H-5", "title": "Guru Teg Bahadur (GTB)", "type": "Hospital", "coords": [28.6833, 77.3072], "radius": 0.5, "color": "#ef4444", "message": "Public Health Zone: Strict Silence required. No honking." },
        { "id": "GF-H-6", "title": "G.B. Pant Hospital", "type": "Hospital", "coords": [28.6375, 77.2355], "radius": 0.5, "color": "#ef4444", "message": "Public Health Zone: Strict Silence required. No honking." },
        { "id": "GF-H-7", "title": "Deen Dayal Upadhyay (DDU)", "type": "Hospital", "coords": [28.6291, 77.1118], "radius": 0.5, "color": "#ef4444", "message": "Public Health Zone: Strict Silence required. No honking." },
        { "id": "GF-H-8", "title": "Dr. Baba Saheb Ambedkar", "type": "Hospital", "coords": [28.7144, 77.1151], "radius": 0.5, "color": "#ef4444", "message": "Public Health Zone: Strict Silence required. No honking." },
        { "id": "GF-H-9", "title": "Lady Hardinge", "type": "Hospital", "coords": [28.6341, 77.2136], "radius": 0.5, "color": "#ef4444", "message": "Public Health Zone: Strict Silence required. No honking." },
        { "id": "GF-H-10", "title": "Chacha Nehru Bal Chikitsalaya", "type": "Hospital", "coords": [28.6617, 77.2644], "radius": 0.5, "color": "#ef4444", "message": "Public Health Zone: Strict Silence required. No honking." },

        # COLLEGES (Blue)
        { "id": "GF-C-1", "title": "St. Stephen's College", "type": "College", "coords": [28.6853, 77.2128], "radius": 0.8, "color": "#3b82f6", "message": "Educational Zone: Drive slowly. Watch out for students." },
        { "id": "GF-C-2", "title": "Hindu College", "type": "College", "coords": [28.6844, 77.2115], "radius": 0.8, "color": "#3b82f6", "message": "Educational Zone: Drive slowly. Watch out for students." },
        { "id": "GF-C-3", "title": "Miranda House", "type": "College", "coords": [28.6888, 77.2107], "radius": 0.8, "color": "#3b82f6", "message": "Educational Zone: Drive slowly. Watch out for students." },
        { "id": "GF-C-4", "title": "Hansraj College", "type": "College", "coords": [28.6795, 77.2110], "radius": 0.8, "color": "#3b82f6", "message": "Educational Zone: Drive slowly. Watch out for students." },
        { "id": "GF-C-5", "title": "Shri Ram College of Commerce", "type": "College", "coords": [28.6828, 77.2139], "radius": 0.8, "color": "#3b82f6", "message": "Educational Zone: Drive slowly. Watch out for students." },
        { "id": "GF-C-6", "title": "Netaji Subhas University", "type": "College", "coords": [28.6091, 77.0375], "radius": 0.8, "color": "#3b82f6", "message": "Educational Zone: Drive slowly. Watch out for students." },
        { "id": "GF-C-7", "title": "Delhi Technological University", "type": "College", "coords": [28.7501, 77.1177], "radius": 0.8, "color": "#3b82f6", "message": "Educational Zone: Drive slowly. Watch out for students." },
        { "id": "GF-C-8", "title": "Lady Shri Ram College", "type": "College", "coords": [28.5620, 77.2403], "radius": 0.8, "color": "#3b82f6", "message": "Educational Zone: Drive slowly. Watch out for students." },
        { "id": "GF-C-9", "title": "Kirori Mal College", "type": "College", "coords": [28.6852, 77.2110], "radius": 0.8, "color": "#3b82f6", "message": "Educational Zone: Drive slowly. Watch out for students." },
        { "id": "GF-C-10", "title": "Shaheed Sukhdev College", "type": "College", "coords": [28.7326, 77.1176], "radius": 0.8, "color": "#3b82f6", "message": "Educational Zone: Drive slowly. Watch out for students." },

        # BRIDGES (Orange)
        { "id": "GF-B-1", "title": "Signature Bridge", "type": "Bridge", "coords": [28.7032, 77.2312], "radius": 1.0, "color": "#f97316", "message": "High Traffic Bridge: Speed strictly enforced. Do not park on the bridge." },
        { "id": "GF-B-2", "title": "Old Yamuna Bridge", "type": "Bridge", "coords": [28.6619, 77.2483], "radius": 1.0, "color": "#f97316", "message": "High Traffic Bridge: Speed strictly enforced. Do not park on the bridge." },
        { "id": "GF-B-3", "title": "Nizamuddin Bridge", "type": "Bridge", "coords": [28.5898, 77.2689], "radius": 1.0, "color": "#f97316", "message": "High Traffic Bridge: Speed strictly enforced. Do not park on the bridge." },
        { "id": "GF-B-4", "title": "Wazirabad Barrage", "type": "Bridge", "coords": [28.7136, 77.2291], "radius": 1.0, "color": "#f97316", "message": "High Traffic Bridge: Speed strictly enforced. Do not park on the bridge." },
        { "id": "GF-B-5", "title": "ITO Barrage Bridge", "type": "Bridge", "coords": [28.6315, 77.2494], "radius": 1.0, "color": "#f97316", "message": "High Traffic Bridge: Speed strictly enforced. Do not park on the bridge." },
        { "id": "GF-B-6", "title": "DND Flyway Bridge", "type": "Bridge", "coords": [28.5724, 77.2648], "radius": 1.0, "color": "#f97316", "message": "High Traffic Bridge: Speed strictly enforced. Do not park on the bridge." },
        { "id": "GF-B-7", "title": "Geeta Colony Bridge", "type": "Bridge", "coords": [28.6625, 77.2642], "radius": 1.0, "color": "#f97316", "message": "High Traffic Bridge: Speed strictly enforced. Do not park on the bridge." },
        { "id": "GF-B-8", "title": "Vikas Marg Bridge", "type": "Bridge", "coords": [28.6306, 77.2497], "radius": 1.0, "color": "#f97316", "message": "High Traffic Bridge: Speed strictly enforced. Do not park on the bridge." },

        # INFRASTRUCTURE PROJECTS (Purple)
        { "id": "GF-P-1", "title": "Central Vista Redevelopment", "type": "Infrastructure", "coords": [28.6125, 77.2111], "radius": 1.5, "color": "#8b5cf6", "message": "Heavy Construction Zone: Caution advised. Follow designated detours." },
        { "id": "GF-P-2", "title": "Dwarka Expressway", "type": "Infrastructure", "coords": [28.5552, 77.0270], "radius": 1.5, "color": "#8b5cf6", "message": "Heavy Construction Zone: Caution advised. Follow designated detours." },
        { "id": "GF-P-3", "title": "Delhi-Meerut RRTS Corridor", "type": "Infrastructure", "coords": [28.5912, 77.2514], "radius": 1.5, "color": "#8b5cf6", "message": "Heavy Construction Zone: Caution advised. Follow designated detours." },
        { "id": "GF-P-4", "title": "New Delhi Railway Station", "type": "Infrastructure", "coords": [28.6419, 77.2215], "radius": 1.5, "color": "#8b5cf6", "message": "Heavy Construction Zone: Caution advised. Follow designated detours." },
        { "id": "GF-P-5", "title": "Delhi Airport Expansion", "type": "Infrastructure", "coords": [28.5562, 77.0999], "radius": 1.5, "color": "#8b5cf6", "message": "Heavy Construction Zone: Caution advised. Follow designated detours." },
        { "id": "GF-P-6", "title": "Urban Extension Road II", "type": "Infrastructure", "coords": [28.5800, 77.0100], "radius": 1.5, "color": "#8b5cf6", "message": "Heavy Construction Zone: Caution advised. Follow designated detours." }
    ]

    # Delete existing docs if any
    geofences_ref = db.collection('geofences')
    for doc in geofences_ref.stream():
        doc.reference.delete()

    for gf in geofences:
        doc_id = gf.pop('id')
        geofences_ref.document(doc_id).set(gf)
        print(f"Added geofence: {doc_id}")

    print("Database seeding completed.")

if __name__ == "__main__":
    seed_database()
