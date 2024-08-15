var map = L.map('map').setView([4.5981, -74.0760], 7); // Coordenadas centradas en Colombia
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

function updateMap() {
    var region = document.getElementById('region').value;
    var start = document.getElementById('start').value;
    var end = document.getElementById('end').value;
    fetch(`/avistamientos?region=${region}&start=${start}&end=${end}`)
        .then(response => response.json())
        .then(data => {
            map.eachLayer(function (layer) {
                if (layer instanceof L.Marker) {
                    map.removeLayer(layer);
                }
            });
            data.forEach(function (ave) {
                if (ave.lat && ave.lng) {
                    var marker = L.marker([ave.lat, ave.lng]).addTo(map);
                    marker.bindPopup(`<strong>Especie:</strong> ${ave.comName}<br><strong>Fecha:</strong> ${ave.obsDt}`);
                }
            });
            var myModal = new bootstrap.Modal(document.getElementById('mapModal'), {
                keyboard: false
            });
            myModal.show();
            myModal._element.addEventListener('shown.bs.modal', function () {
                map.invalidateSize(); // Esto recalcula el tamaño del mapa
            });
        })
        .catch(error => console.error('Error al cargar los datos:', error));
}