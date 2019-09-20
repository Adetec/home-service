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
        url: "/API/1.0/services",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (response) {
            response.forEach(service => {
                console.log(service.id, service.service_name, service.lat, service.lon);
                let geoFeature = {
                    "type": "Feature",
                    "properties": {
                        "message": service.service_name,
                        "image": service.owner_image,
                        "owner": service.owner,
                        "iconSize": [60, 60]
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            service.lon,
                            service.lat
                        ]
                    }
                }
                geojson.features.push(geoFeature)
                /* mainMap.loadImage(`static/img/users-profile/${service.owner_image}`, function(error, image) {
                    if (error) throw error;
                    mainMap.addImage(`cat-${service.id}`, image);
                    mainMap.addLayer({
                        "id": `points-${service.id}`,
                        "type": "symbol",
                        "source": {
                            "type": "geojson",
                            "data": {
                                "type": "FeatureCollection",
                                "features": [{
                                    "type": "Feature",
                                    "geometry": {
                                    "type": "Point",
                                    "coordinates": [service.lon, service.lat]
                                    }
                                }]
                            }
                        },
                        "layout": {
                            "icon-image": `cat-${service.id}`,
                            "icon-size": 0.15
                        }
                    });
                }); */
            });
            geojson.features.forEach(function(marker) {
                // create a DOM element for the marker
                var el = document.createElement('div');
                el.className = 'marker';
                el.style.backgroundImage = `url(static/img/users-profile/${marker.properties.image}`;
                el.style.width = marker.properties.iconSize[0] + 'px';
                el.style.height = marker.properties.iconSize[1] + 'px';
                el.style.backgroundSize = 'cover'
                 
                el.addEventListener('click', function() {
                    geojson.features.forEach((m) => {
                        if (m.properties.owner == marker.properties.owner) {
                            let modal, modalDialog, modalContent;

                            modal = document.createElement('div');
                            modalDialog = document.createElement('div');
                            modalContent = document.createElement('div');

                            modal.classList.add('modal', 'fade', 'bd-example-modal-lg');
                            modalDialog.classList.add('modal-dialog', 'modal-lg');
                            modalContent.classList.add('modal-content');
                            modalContent.textContent = '{{ current_user.username }}';
                            modalDialog.appendChild(modalContent);
                            modal.appendChild(modalDialog);
                            $(modal).modal('toggle')
                            
                            console.log(modal);
                        }

                    })
                    
                // window.alert(marker.properties.message);
                });
                 
                // add marker to map
                new mapboxgl.Marker(el)
                .setLngLat(marker.geometry.coordinates)
                .addTo(mainMap);
                });
        }
    });
})
