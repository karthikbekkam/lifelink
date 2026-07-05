window.onload = function () {

    // Create map with a default location (Vijayawada)
    const map = L.map("map").setView([16.5062, 80.6480], 12);

    // OpenStreetMap Layer
    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution: "&copy; OpenStreetMap contributors",
            maxZoom: 19
        }
    ).addTo(map);

    // ==============================
    // LifeLink Center
    // ==============================

    L.marker([16.5062, 80.6480])
        .addTo(map)
        .bindPopup("<b>🩸 LifeLink Center</b><br>Vijayawada");

    // ==============================
    // Hospitals
    // ==============================

    L.marker([16.5068, 80.6488])
        .addTo(map)
        .bindPopup("<b>🏥 Apollo Hospital</b>");

    L.marker([16.4300, 80.5600])
        .addTo(map)
        .bindPopup("<b>🏥 AIIMS Mangalagiri</b>");

    L.marker([16.5150, 80.6400])
        .addTo(map)
        .bindPopup("<b>🏥 Government General Hospital</b>");

    // ==============================
    // User Location
    // ==============================

    if (!navigator.geolocation) {

        alert("Geolocation is not supported by this browser.");

        return;

    }

    navigator.geolocation.getCurrentPosition(

        function (position) {

            const lat = position.coords.latitude;
            const lng = position.coords.longitude;

            // User Marker
            L.marker([lat, lng])
                .addTo(map)
                .bindPopup("<b>📍 You are here</b>")
                .openPopup();

            // Search Radius
            L.circle([lat, lng], {
                radius: 5000,
                color: "red",
                fillColor: "#ff6666",
                fillOpacity: 0.2
            }).addTo(map);

            // Move map to user
            map.setView([lat, lng], 13);

        },

        function (error) {

            console.log(error);

            alert("Location permission denied. Showing default map.");

        }

    );

};