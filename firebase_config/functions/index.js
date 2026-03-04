const { onDocumentUpdated } = require("firebase-functions/v2/firestore");
const admin = require("firebase-admin");

admin.initializeApp();

exports.onProjectVerified = onDocumentUpdated("projects/{projectId}", async (event) => {
    const beforeData = event.data.before.data();
    const afterData = event.data.after.data();

    // Check if status changed to 'Verified'
    if (afterData.status === 'Verified' && beforeData.status !== 'Verified') {
        const projectCoords = afterData.coords; // Assuming [lat, lng] array
        if (!projectCoords) {
            console.log("No coords found for project", event.params.projectId);
            return;
        }

        const projectLat = projectCoords[0];
        const projectLng = projectCoords[1];

        // Fetch users from users collection
        const usersSnapshot = await admin.firestore().collection("users").get();
        const notificationPromises = [];

        usersSnapshot.forEach((userDoc) => {
            const userData = userDoc.data();
            const userCoords = userData.current_location;

            // Proceed only if user has a location and FCM token
            if (userCoords && userData.fcm_token) {
                let userLat, userLng;

                // Support multiple coordinate formats for flexibility
                if (Array.isArray(userCoords)) {
                    userLat = userCoords[0];
                    userLng = userCoords[1];
                } else if (userCoords.latitude && userCoords.longitude) {
                    userLat = userCoords.latitude;
                    userLng = userCoords.longitude;
                }

                if (userLat && userLng) {
                    const distance = getDistanceFromLatLonInKm(projectLat, projectLng, userLat, userLng);

                    // Filter: within a 1 km radius
                    if (distance <= 1.0) {
                        const payload = {
                            token: userData.fcm_token,
                            notification: {
                                title: `Accountability Delivered: ${afterData.title || 'Project'} is Fixed!`,
                                body: "Tap to see the 'Before' and 'After' image proof."
                            },
                            data: {
                                beforeImageUrl: afterData.beforeImageUrl || afterData.imageUrl || "", // fallback mapping
                                afterImageUrl: afterData.afterImageUrl || "",
                                projectId: event.params.projectId
                            }
                        };

                        notificationPromises.push(admin.messaging().send(payload));
                    }
                }
            }
        });

        // Send all FCM pushes concurrently
        if (notificationPromises.length > 0) {
            await Promise.allSettled(notificationPromises);
            console.log(`Successfully sent ${notificationPromises.length} notifications to citizens within 1km of project ${event.params.projectId}`);
        } else {
            console.log("No users found within 1km radius.");
        }
    }
});

// Helper: Haversine distance formula
function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
    const R = 6371; // Radius of the earth in km
    const dLat = deg2rad(lat2 - lat1);
    const dLon = deg2rad(lon2 - lon1);
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const d = R * c; // Distance in km
    return d;
}

function deg2rad(deg) {
    return deg * (Math.PI / 180);
}
