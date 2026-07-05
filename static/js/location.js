// =====================================
// Get Current User Location
// =====================================

function getLocation() {

    if (navigator.geolocation) {

        navigator.geolocation.getCurrentPosition(

            showPosition,

            showError

        );

    }

    else {

        alert("Geolocation is not supported by this browser.");

    }

}

// =====================================

function showPosition(position) {

    const latitude = position.coords.latitude;

    const longitude = position.coords.longitude;

    console.log(latitude);

    console.log(longitude);

    document.getElementById("latitude").value = latitude;

    document.getElementById("longitude").value = longitude;

}

// =====================================

function showError(error) {

    alert("Unable to fetch location.");

}