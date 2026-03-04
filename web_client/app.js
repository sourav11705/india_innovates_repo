// Default Firebase configuration for the pre-initialized project
const firebaseConfig = {
    projectId: 'testapphack', // Since we are largely just saving data, we primarily need the project ID if using default auth, but realistically we need fully initialized app for web client.
    // For demo purposes, we will rely on a generic initialization assuming no strict rules for write for now, or we'd need actual credentials.
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

// Existing Geofences
const GEOFENCES = [
    // HOSPITALS (Red)
    { id: "GF-H-1", title: "AIIMS New Delhi", type: "Hospital", coords: [28.5672, 77.2100], radius: 0.5, color: "#d9534f", message: "Public Health Zone: Strict Silence required. No honking." },
    { id: "GF-H-2", title: "Safdarjung Hospital", type: "Hospital", coords: [28.5663, 77.2075], radius: 0.5, color: "#d9534f", message: "Public Health Zone: Strict Silence required. No honking." },
    { id: "GF-H-3", title: "Ram Manohar Lohia (RML)", type: "Hospital", coords: [28.6253, 77.2013], radius: 0.5, color: "#d9534f", message: "Public Health Zone: Strict Silence required. No honking." },
    { id: "GF-H-4", title: "Lok Nayak Hospital (LNJP)", type: "Hospital", coords: [28.6366, 77.2343], radius: 0.5, color: "#d9534f", message: "Public Health Zone: Strict Silence required. No honking." },
    { id: "GF-H-5", title: "Guru Teg Bahadur (GTB)", type: "Hospital", coords: [28.6833, 77.3072], radius: 0.5, color: "#d9534f", message: "Public Health Zone: Strict Silence required. No honking." },
    { id: "GF-H-6", title: "G.B. Pant Hospital", type: "Hospital", coords: [28.6375, 77.2355], radius: 0.5, color: "#d9534f", message: "Public Health Zone: Strict Silence required. No honking." },
    { id: "GF-H-7", title: "Deen Dayal Upadhyay (DDU)", type: "Hospital", coords: [28.6291, 77.1118], radius: 0.5, color: "#d9534f", message: "Public Health Zone: Strict Silence required. No honking." },
    { id: "GF-H-8", title: "Dr. Baba Saheb Ambedkar", type: "Hospital", coords: [28.7144, 77.1151], radius: 0.5, color: "#d9534f", message: "Public Health Zone: Strict Silence required. No honking." },
    { id: "GF-H-9", title: "Lady Hardinge", type: "Hospital", coords: [28.6341, 77.2136], radius: 0.5, color: "#d9534f", message: "Public Health Zone: Strict Silence required. No honking." },
    { id: "GF-H-10", title: "Chacha Nehru Bal Chikitsalaya", type: "Hospital", coords: [28.6617, 77.2644], radius: 0.5, color: "#d9534f", message: "Public Health Zone: Strict Silence required. No honking." },

    // COLLEGES (Blue)
    { id: "GF-C-1", title: "St. Stephen's College", type: "College", coords: [28.6853, 77.2128], radius: 0.8, color: "#0275d8", message: "Educational Zone: Drive slowly. Watch out for students." },
    { id: "GF-C-2", title: "Hindu College", type: "College", coords: [28.6844, 77.2115], radius: 0.8, color: "#0275d8", message: "Educational Zone: Drive slowly. Watch out for students." },
    { id: "GF-C-3", title: "Miranda House", type: "College", coords: [28.6888, 77.2107], radius: 0.8, color: "#0275d8", message: "Educational Zone: Drive slowly. Watch out for students." },
    { id: "GF-C-4", title: "Hansraj College", type: "College", coords: [28.6795, 77.2110], radius: 0.8, color: "#0275d8", message: "Educational Zone: Drive slowly. Watch out for students." },
    { id: "GF-C-5", title: "Shri Ram College of Commerce", type: "College", coords: [28.6828, 77.2139], radius: 0.8, color: "#0275d8", message: "Educational Zone: Drive slowly. Watch out for students." },
    { id: "GF-C-6", title: "Netaji Subhas University", type: "College", coords: [28.6091, 77.0375], radius: 0.8, color: "#0275d8", message: "Educational Zone: Drive slowly. Watch out for students." },
    { id: "GF-C-7", title: "Delhi Technological University", type: "College", coords: [28.7501, 77.1177], radius: 0.8, color: "#0275d8", message: "Educational Zone: Drive slowly. Watch out for students." },
    { id: "GF-C-8", title: "Lady Shri Ram College", type: "College", coords: [28.5620, 77.2403], radius: 0.8, color: "#0275d8", message: "Educational Zone: Drive slowly. Watch out for students." },
    { id: "GF-C-9", title: "Kirori Mal College", type: "College", coords: [28.6852, 77.2110], radius: 0.8, color: "#0275d8", message: "Educational Zone: Drive slowly. Watch out for students." },
    { id: "GF-C-10", title: "Shaheed Sukhdev College", "type": "College", coords: [28.7326, 77.1176], radius: 0.8, color: "#0275d8", message: "Educational Zone: Drive slowly. Watch out for students." },

    // BRIDGES (Orange)
    { id: "GF-B-1", title: "Signature Bridge", type: "Bridge", coords: [28.7032, 77.2312], radius: 1.0, color: "#f0ad4e", message: "High Traffic Bridge: Speed strictly enforced. Do not park on the bridge." },
    { id: "GF-B-2", title: "Old Yamuna Bridge", type: "Bridge", coords: [28.6619, 77.2483], radius: 1.0, color: "#f0ad4e", message: "High Traffic Bridge: Speed strictly enforced. Do not park on the bridge." },
    { id: "GF-B-3", title: "Nizamuddin Bridge", type: "Bridge", coords: [28.5898, 77.2689], radius: 1.0, color: "#f0ad4e", message: "High Traffic Bridge: Speed strictly enforced. Do not park on the bridge." },
    { id: "GF-B-4", title: "Wazirabad Barrage", type: "Bridge", coords: [28.7136, 77.2291], radius: 1.0, color: "#f0ad4e", message: "High Traffic Bridge: Speed strictly enforced. Do not park on the bridge." },
    { id: "GF-B-5", title: "ITO Barrage Bridge", type: "Bridge", coords: [28.6315, 77.2494], radius: 1.0, color: "#f0ad4e", message: "High Traffic Bridge: Speed strictly enforced. Do not park on the bridge." },
    { id: "GF-B-6", title: "DND Flyway Bridge", type: "Bridge", coords: [28.5724, 77.2648], radius: 1.0, color: "#f0ad4e", message: "High Traffic Bridge: Speed strictly enforced. Do not park on the bridge." },
    { id: "GF-B-7", title: "Geeta Colony Bridge", type: "Bridge", coords: [28.6625, 77.2642], radius: 1.0, color: "#f0ad4e", message: "High Traffic Bridge: Speed strictly enforced. Do not park on the bridge." },
    { id: "GF-B-8", title: "Vikas Marg Bridge", type: "Bridge", coords: [28.6306, 77.2497], radius: 1.0, color: "#f0ad4e", message: "High Traffic Bridge: Speed strictly enforced. Do not park on the bridge." },

    // INFRASTRUCTURE PROJECTS (Purple)
    { id: "GF-P-1", title: "Central Vista Redevelopment", type: "Infrastructure", coords: [28.6125, 77.2111], radius: 1.5, color: "#5bc0de", message: "Heavy Construction Zone: Caution advised. Follow designated detours." },
    { id: "GF-P-2", "title": "Dwarka Expressway", "type": "Infrastructure", "coords": [28.5552, 77.0270], radius: 1.5, color: "#5bc0de", message: "Heavy Construction Zone: Caution advised. Follow designated detours." },
    { id: "GF-P-3", "title": "Delhi-Meerut RRTS Corridor", "type": "Infrastructure", "coords": [28.5912, 77.2514], radius: 1.5, color: "#5bc0de", message: "Heavy Construction Zone: Caution advised. Follow designated detours." },
    { id: "GF-P-4", "title": "New Delhi Railway Station", "type": "Infrastructure", "coords": [28.6419, 77.2215], radius: 1.5, color: "#5bc0de", message: "Heavy Construction Zone: Caution advised. Follow designated detours." },
    { id: "GF-P-5", "title": "Delhi Airport Expansion", "type": "Infrastructure", "coords": [28.5562, 77.0999], radius: 1.5, color: "#5bc0de", message: "Heavy Construction Zone: Caution advised. Follow designated detours." },
    { id: "GF-P-6", "title": "Urban Extension Road II", "type": "Infrastructure", "coords": [28.5800, 77.0100], radius: 1.5, color: "#5bc0de", message: "Heavy Construction Zone: Caution advised. Follow designated detours." }
];

let activeGeofences = new Map(); // Store full gf objects by id
let map;
let userMarker;
let geofenceCircles = [];
let currentActiveGeofenceForFeedback = null;
let uploadedPhotoBase64 = null;

// DOM Elements
const btn = document.getElementById("enableBtn");
const locationText = document.getElementById("locationText");
const logList = document.getElementById("logList");

// Banner Elements
// Banner Elements
const alertBanner = document.getElementById("alertBanner");
const alertTitle = document.getElementById("alertTitle");
const alertMessage = document.getElementById("alertMessage");


// Default center (New Delhi)
const INITIAL_LAT = 28.6139;
const INITIAL_LNG = 77.2090;
let currentCoords = [INITIAL_LAT, INITIAL_LNG];

function initMap() {
    map = L.map('map').setView([INITIAL_LAT, INITIAL_LNG], 11);

    // Standard OpenStreetMap tiles for a conventional look
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OSM</a>'
    }).addTo(map);

    GEOFENCES.forEach(renderGeofence);

    const userIcon = L.divIcon({
        html: '🚶‍♂️',
        iconSize: [30, 30],
        className: 'user-marker'
    });

    userMarker = L.marker([INITIAL_LAT, INITIAL_LNG], {
        icon: userIcon,
        draggable: true,
        zIndexOffset: 1000
    }).addTo(map);

    userMarker.bindPopup("<b>Simulated User</b><br>Drag to move into civic zones.").openPopup();

    userMarker.on('dragend', function (event) {
        const marker = event.target;
        const position = marker.getLatLng();
        handleNewPosition(position.lat, position.lng, "Simulated");
    });

    handleNewPosition(INITIAL_LAT, INITIAL_LNG, "Initial");
}

function renderGeofence(gf) {
    const circle = L.circle(gf.coords, {
        color: gf.color,
        fillColor: gf.color,
        fillOpacity: 0.15, // Lighter for conventional map
        weight: 2,
        radius: gf.radius * 1000
    }).addTo(map);

    circle.bindPopup(`<b>${gf.title}</b><br>${gf.message}`);
    geofenceCircles.push(circle);
}

function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
}

function handleNewPosition(lat, lng, source) {
    currentCoords = [lat, lng];
    locationText.innerText = `Pos: ${lat.toFixed(4)}, ${lng.toFixed(4)} (${source})`;

    let insideList = [];

    GEOFENCES.forEach(gf => {
        const distanceKm = getDistanceFromLatLonInKm(lat, lng, gf.coords[0], gf.coords[1]);

        if (distanceKm <= gf.radius) {
            insideList.push(gf);
            if (!activeGeofences.has(gf.id)) {
                activeGeofences.set(gf.id, gf);
                triggerNotification(gf);
            }
        } else {
            if (activeGeofences.has(gf.id)) {
                activeGeofences.delete(gf.id);
            }
        }
    });

    updateBannerUI(insideList.length > 0 ? insideList[0] : null);
}

function updateBannerUI(primaryGf) {
    if (primaryGf) {
        alertBanner.classList.remove("hidden");
        alertTitle.innerText = `Active Zone: ${primaryGf.title}`;
        alertMessage.innerText = primaryGf.message;
        alertBanner.style.backgroundColor = `rgba(255, 243, 205, 0.8)`; // light yellow warning
        alertBanner.style.borderLeft = `5px solid ${primaryGf.color}`;

    } else {
        alertBanner.classList.add("hidden");
    }
}

function triggerNotification(gf) {
    const li = document.createElement("li");
    li.innerHTML = `<strong>[Entered] ${gf.title}:</strong> ${gf.message}`;

    const emptyLog = document.querySelector(".empty-log");
    if (emptyLog) emptyLog.remove();

    logList.prepend(li);

    if ("Notification" in window && Notification.permission === "granted") {
        new Notification(`⚠️ ${gf.title}`, {
            body: gf.message
        });
    }
}

btn.addEventListener("click", async (e) => {
    e.preventDefault();
    if ("Notification" in window) {
        const perm = await Notification.requestPermission();
        if (perm === "granted") {
            btn.innerText = "Location Services Active";
            btn.style.color = "#28a745";
        }
    }
});

document.addEventListener('DOMContentLoaded', initMap);
