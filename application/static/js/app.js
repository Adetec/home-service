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

    // Animate counting
    $('.counter-value').each(function () {
        const $this = $(this);
        jQuery({ Counter: 0 }).animate({ Counter: $this.text() }, {
          duration: 3500,
          easing: 'swing',
          step: function () {
            $this.text(Math.ceil(this.Counter));
            $this.toggleClass('animated flash')
          }
        });
    });
    
});

// Get notifications
let getNot = setInterval(() => {
    $.ajax({
        type: "GET",
        url: "/API/1.0/notifications",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (response) {
            response.forEach(notifications => {
                console.log(notifications.notifications);
                renderNotifications(notifications.notifications)
                $('#notif-badge').text(notifications.notifications.length)
            });
        }
    });
}, 5000)

const renderNotifications =(notifs) => {
   let container = $('#notifs-list')
   $(container).children().remove();
   notifs.forEach(notif => {
       let notElement = document.createElement('a');
       let sender = document.createElement('small');
       let msgTime = document.createElement('small');
       let url = `/request_service/${notif.client_id}/${notif.service_request_id}/new#msg-${notif.message_id}`
       $(notElement).attr('href', url);
       $(notElement).addClass('dropdown-item');
       $(sender).addClass('text-primary');
       $(msgTime).addClass('text-muted');
       $(sender).text(notif.sender);
       $(notElement).text(` ${notif.message} `);
       $(msgTime).text(moment(notif.created_at).fromNow());
       $(notElement).prepend(sender);
       $(notElement).append(msgTime);
       $(container).append(notElement);
   });
}

var geojson = {
    "type": "FeatureCollection",
    "features": []
};

// Create the main map
mapboxgl.accessToken = 'pk.eyJ1IjoiaG9tZXNlcnZpY2UiLCJhIjoiY2swcGh4eTk5MDEzczNtcG9laGh5eWx1biJ9.3FOluiVDosFsTuG9Ps6YGw';
let mainMap = new mapboxgl.Map({
    container: 'main-map',
    style: 'mapbox://styles/homeservice/ck0r75ecu0las1cn2e454xnow',
    center: [6.094710824465892, 35.53808204473481],
    zoom: 11
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
                        "iconSize": [45, 45]
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
                markerElement.style.backgroundSize = 'cover';
                
                 
                markerElement.addEventListener('click', function() {
                    

                    serviceToast = document.createElement('div');
                    serviceToast.classList.add('toast');
                    serviceToast.setAttribute('data-delay', '20000');
                    
                    serviceToastHeader = document.createElement('div');
                    serviceToastHeader.textContent = marker.properties.owner
                    serviceToastHeader.classList.add('toast-header');

                    serviceToastBody = document.createElement('div');
                    serviceToastBody.classList.add('toast-body');

                    servicesLst = document.createElement('div');
                    servicesLst.classList.add('text-right');

                    marker.properties.services.forEach(service => {

                        let serviceList = document.createElement('div');
                        serviceList.classList.add('text-right');

                        let serviceLink = document.createElement('a');
                        serviceLink.setAttribute('href',`/service/${service.id}`);
                        serviceLink.textContent = service.service_name

                        serviceList.appendChild(serviceLink)
                        servicesLst.appendChild(serviceList);
                    });
                    
                    serviceToastBody.appendChild(servicesLst)
                    serviceToast.appendChild(serviceToastHeader);
                    serviceToast.appendChild(serviceToastBody);
                    console.log($(serviceToast));
                    $('.toast').remove();
                    $(markerElement).append(serviceToast);
                    $('.toast').toast('show');
                    
                    
                    
                    // console.log(serviceToast);
                    
                // window.alert(marker.properties.message);
                });

                // create the service owner marker icon
                new mapboxgl.Marker()
                .setLngLat(marker.geometry.coordinates)
                .addTo(mainMap)
                
                // create a marker icon & add it to the map
                new mapboxgl.Marker(markerElement)
                .setLngLat(marker.geometry.coordinates)
                .addTo(mainMap);
                });
        }
    });
})
