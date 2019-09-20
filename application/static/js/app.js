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


var geojson = {
    "type": "FeatureCollection",
    "features": []
};

// Create the main map
mapboxgl.accessToken = 'pk.eyJ1IjoiaG9tZXNlcnZpY2UiLCJhIjoiY2swcGh4eTk5MDEzczNtcG9laGh5eWx1biJ9.3FOluiVDosFsTuG9Ps6YGw';
let mainMap = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/homeservice/ck0r75ecu0las1cn2e454xnow',
    center: [6.094710824465892, 35.53808204473481],
    zoom: 9
});

// Add zoom and rotation controls to the map.
mainMap.addControl(new mapboxgl.NavigationControl());

mainMap.on('load', () => {
    // get services users geo cordinates:
    $.ajax({
        type: "GET",
        url: "/API/1.0/owners",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (response) {
            response.forEach(owner => {
                console.log(owner.id);
                let geoFeature = {
                    "type": "Feature",
                    "properties": {
                        "userId": owner.id,
                        "image": owner.owner_image,
                        "owner": owner.owner,
                        "services": owner.services,
                        "iconSize": [60, 60]
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            owner.lon,
                            owner.lat
                        ]
                    }
                }
                geojson.features.push(geoFeature)
                
            });
            geojson.features.forEach(function(marker) {
                // create a DOM element for the marker
                let markerElement = document.createElement('div');
                markerElement.classList.add('marker');
                markerElement.style.backgroundImage = `url(static/img/users-profile/${marker.properties.image}`;
                markerElement.style.width = marker.properties.iconSize[0] + 'px';
                markerElement.style.height = marker.properties.iconSize[1] + 'px';
                markerElement.style.backgroundSize = 'cover'
                 
                markerElement.addEventListener('click', function() {
                    let modal, modalDialog, modalContent;

                    servicesLst = document.createElement('ul');
                    modal = document.createElement('div');
                    modalDialog = document.createElement('div');
                    modalContent = document.createElement('div');

                    marker.properties.services.forEach(service => {
                        let serviceList = document.createElement('li');
                        serviceList.textContent = service.service_name
                        console.log(service.service_name);
                        servicesLst.appendChild(serviceList);
                    });
                    modal.classList.add('modal', 'fade', 'bd-example-modal-lg');
                    modalDialog.classList.add('modal-dialog', 'modal-lg');
                    modalContent.classList.add('modal-content');
                    modalContent.appendChild(servicesLst);
                    modalDialog.appendChild(modalContent);
                    modal.appendChild(modalDialog);
                    $(modal).modal('toggle')
                    
                    console.log(modal);
                    
                // window.alert(marker.properties.message);
                });
                 
                // add marker to map
                new mapboxgl.Marker(markerElement)
                .setLngLat(marker.geometry.coordinates)
                .addTo(mainMap);
                });
        }
    });
})
