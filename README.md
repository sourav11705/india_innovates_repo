# 📍 KshetraRakshak (Geofence Guardian)

KshetraRakshak is a modern, lightweight Progressive Web Application (PWA) designed to foster civic responsibility and streamline public infrastructure reporting without the friction of app store installations. 

By leveraging native HTML5 Geolocation and Web Push API natively in the browser, KshetraRakshak dynamically detects when a citizen enters critical public infrastructure zones in New Delhi and fires contextual push notifications directly to their smartphone, while centralizing public issue reporting on a dedicated Administrative Web Platform.

## 🌟 The Core Workflows

KshetraRakshak caters to two primary audiences: the **Citizens on the Ground** and the **Authorities in the Control Room**.

### 📱 1. The Citizen Experience (Mobile Browser Workflow)
No mobile app downloads are required. The citizen experience is entirely web-based for maximum adoption.
1.  **Onboarding**: The citizen navigates to the KshetraRakshak web URL on their phone's browser (e.g., Chrome or Safari).
2.  **Opt-In**: They click **"Enable Location Services"** and grant the browser permission to track their location and send push notifications.
3.  **Passive Monitoring**: The citizen can now put their phone in their pocket or mount it on their dashboard. The website runs purely in the background.
4.  **Zone Breach (The Trigger)**: As the citizen physically travels through the city, the system's Haversine algorithm continuously checks their coordinates against 34 predefined "Civic Zones".
5.  **Contextual Notification**: If the citizen crosses the boundary of a 500-meter radius around *Safdarjung Hospital*, a native OS push notification immediately pops up on their phone reading: *"Public Health Zone: Strict Silence required. No honking."*
6.  **Public Empowerment**: The PWA acts as a passive guardian, reminding citizens of regional rules precisely when they need to hear them.

### 🏛️ 2. The Authority Experience (Desktop Dashboard Workflow)
The same URL adapts beautifully to a desktop screen, serving as the Command Center for city officials.
1.  **Live Civic Zoning Map**: Authorities are presented with a Dark-Mode Leaflet interactive map of New Delhi, clearly displaying all 34 active Geofences divided by type:
    *   🔴 **Hospitals (500m radius)**
    *   🔵 **Colleges (800m radius)**
    *   🟠 **Bridges (1km radius)**
    *   🟣 **Infrastructure Projects (1.5km radius)**
2.  **Issue Reports Monitoring**: If a citizen inside a zone spots a broken infrastructure (like potholes on a bridge), they can take a picture on the ground. This gets routed to the **"Issue Reports"** public dashboard page (`reports.html`), allowing authorities to see the attached proof, the exact zone name, and the severity of the infrastructure damage.
3.  **Live Demonstration Simulator**: Authorities can demo the entire Citizen workflow right from their desk. By dragging the 🚶‍♂️ simulator marker directly into a colored boundary on the map, the website artificially simulates a GPS breach and triggers the native OS Push Notification on their desktop instantly!

## 🗂️ Technical Architecture

*   **Frontend Map Engine**: Leaflet.js rendering OpenStreetMap tiles.
*   **Location Tracking Engine**: Vanilla JavaScript hooking into `navigator.geolocation.watchPosition` with a custom Haversine Distance Calculator constrainer (`getDistanceFromLatLonInKm`).
*   **Notification Engine**: Native Browser `Notification` Object.
*   **Backend / Database**: Google Firebase Firestore (used to persistently track Issue Reports globally).
*   **Design Language**: Clean, modern CSS with a non-obtrusive, conventional structure replacing bulky "mobile-app-like" black borders to favor transparency and scalability.

## 🚀 How to Run Locally

### Prerequisites
- Python 3.8+
- Node.js (for Cloud Functions, optional)
- A Firebase project with Firestore enabled
- `serviceAccountKey.json` placed in the root directory (for backend tools)

### 1. View Mobile Client (PWA)
The citizen interface requires no build steps. 
1. Navigate to `web_client/`.
2. Start any local HTTP server: `python -m http.server 8000`
3. View at `http://localhost:8000` (Use `localhost` to allow the browser's Notification API)

### 2. View Authority Dashboard
The Streamlit dashboard allows real-time visualization of reports.
1. Navigate to `admin_dashboard/`.
2. Install dependencies: `pip install -r requirements.txt`
3. Launch dashboard: `streamlit run app.py`
4. View at `http://localhost:8501`

*(To add or tweak the master dataset of geofences into Firebase, use `python scripts/seed_firebase.py`)*

## ⚙️ Project File Structure
```text
KshetraRakshak/
├── admin_dashboard/        # Python Streamlit Control Room
│   ├── app.py              # Main dashboard entry point
│   ├── firebase_utils.py   # Secure Firestore bridge
│   └── components/         # Map and feed rendering modules
├── web_client/             # HTML5 Citizen PWA
│   ├── index.html          # Map and Geofence constraints
│   ├── reports.html        # Public issue reports feed
│   ├── app.js              # Haversine tracking logic & push notifications
│   └── style.css           # Clean, conventional UI styling
├── scripts/                # Database utilities
│   └── seed_firebase.py    # Master dataset seeder (34 pre-defined Delhi limits)
├── firebase_config/        # Security and server configurations
│   ├── firestore.rules     # DB security rules
│   └── functions/          # Firebase Cloud Functions (Push notifications)
└── README.md
```
