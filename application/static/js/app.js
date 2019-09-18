$(document).ready(function(){
    $('.carousel').carousel()

    $('#action-requests').click(() => {
        $('#requests').toggleClass('hide');
    });
    $('#action-services').click(() => {
        $('#services').toggleClass('hide');
    });
    $('#action-edit-profile').click(() => {
        $('#edit-profile').toggleClass('hide');
    });
});

// Mapbox
mapboxgl.accessToken = 'pk.eyJ1IjoiaG9tZXNlcnZpY2UiLCJhIjoiY2swcGh4eTk5MDEzczNtcG9laGh5eWx1biJ9.3FOluiVDosFsTuG9Ps6YGw';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v10',
    center: [6.11, 35.5], // starting position [lng, lat]
    zoom: 15 // starting zoom
});

// Add geolocate control to the map.
map.addControl(new mapboxgl.GeolocateControl({
    positionOptions: {
        enableHighAccuracy: true   
    },
    trackUserLocation: true
}));

map.on('click', function (e) {
    document.getElementById('info').innerHTML =
    // e.point is the x, y coordinates of the mousemove event relative
    // to the top-left corner of the map
    JSON.stringify(e.point) + '<br />' +
    // e.lngLat is the longitude, latitude geographical position of the event
    JSON.stringify(e.lngLat.wrap());
    });
