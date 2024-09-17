var map = L.map('mapid').setView([5.535, -73.367], 8); // Ajusta la ubicación y zoom según necesites

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'legend');
    div.innerHTML += '<b>Convenciones</b><br>';
    div.innerHTML += '<i style="background: #b0df5d; width: 12px; height: 12px; float: left; margin-right: 8px;"></i> Áreas protegidas<br>';
    div.innerHTML += '<i style="background: #f5bd43; width: 12px; height: 12px; float: left; margin-right: 8px;"></i> Rutas de senderismo<br>';
    div.innerHTML += '<i style="background: #be403c; width: 12px; height: 12px; float: left; margin-right: 8px;"></i> Distribución de especies<br>';
    // Añade más ítems según tus capas y datos
    return div;
};

legend.addTo(map);

// Añadir GeoJSON u otras capas aquí
fetch('/biomaexplorer/map/data.geojson')
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        L.geoJson(data, {
            pointToLayer: function(feature, latlng) {
                var iconColor = feature.properties.color;  // Asume que 'color' es una propiedad en tu GeoJSON
                var iconUrl = `http://localhost/biomaexplorer/icon/leaf-${iconColor}.png`;  // Construye la URL del ícono basada en el color
                var shadowUrl = 'http://localhost/biomaexplorer/icon/leaf-shadow.png';  // URL de la sombra

                var customIcon = L.icon({
                    iconUrl: iconUrl,
                    shadowUrl: shadowUrl,
                    iconSize: [38, 95],  // Tamaño del ícono
                    shadowSize: [50, 64],  // Tamaño de la sombra
                    iconAnchor: [22, 94],  // Punto del ícono que corresponderá a la ubicación del marcador
                    shadowAnchor: [4, 62],  // Lo mismo para la sombra
                    popupAnchor: [-3, -76]  // Punto desde el cual se debería abrir el popup relativo al iconAnchor
                });

                return L.marker(latlng, {icon: customIcon});
            },
            onEachFeature: function(feature, layer) {
                if (feature.properties && feature.properties.name) {
                    layer.bindPopup(feature.properties.name + '<br/>' + (feature.properties.description || ''));
                }
            }
        }).addTo(map);
    });



