// Create map and markers
function createMap(locations) {
  // Create a map centered at the first location
  const map = L.map("map").setView([locations[0].latitude, locations[0].longitude], 2);

  // Add a tile layer to display the map
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
      'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
  }).addTo(map);

  // Add markers for each location
  locations.forEach((location) => {
    L.marker([location.latitude, location.longitude]).addTo(map);
  });
}

// Access the globally available locations array
createMap(window.locations);