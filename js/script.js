
let currentPage = document.getElementsByTagName('title')[0].innerText; // Get the current page title
let picture = document.getElementById('picture');


if (currentPage === 'Weekly schedule') {
    
    let elements = []; // store location td elements for image display on moveover
    let eventInfo = [] // store event name, time, and location as an array of objects for google maps and hover display
    let imgs = {
        'Smith': '/images/Smith.png',
        'Zoom': '/images/zoom.jpg',
        'Mayo': '/images/Mayo.png',
        'Keller': '/images/keller.jpg',
        'Church': '/images/Church.png',
        'Free': '/images/freetime.jpg',
        'Sun': '/images/track.jpg'
    };

    let rows = document.querySelectorAll('tbody tr'); // get all the rows except the header rows
    for (let i = 0; i < rows.length; i++) {
        let data = rows[i].getElementsByTagName('td');
        elements.push(data[3]); // store the td element for image display on mouseover
        let eventObj = {
            name: data[1].textContent,
            time: data[2].textContent,
            location: data[3].textContent
        };
        eventInfo.push(eventObj);
        
    }
    //console.log(eventInfo);

    // add event listener to each td element
    elements.forEach((currentTD) => {
        currentTD.addEventListener('mouseover', () => {
            if (!document.getElementById("newImg")) { // not to add multiple images on mouseover
                let newImg = document.createElement("img");
                newImg.src = imgs[currentTD.id];
                newImg.id = "newImg";
                newImg.width = 40;
                newImg.height = 40;
                currentTD.appendChild(newImg);
    
            }
            picture.src = imgs[currentTD.id];
            picture.alt = 'Picture of ' + currentTD.id;
            
        });
        currentTD.addEventListener('mouseout', () => {
            let newImg = document.getElementById("newImg");
            if (newImg) {
                currentTD.removeChild(newImg);
            }
        });
    }); 
    
    // google maps api
    function initMap() {
        let map = new google.maps.Map(document.getElementById("schedule-map"), {
            center: { lat: 44.9727, lng: -93.23540000000003 },
            zoom: 15,
        });
        let geocoder = new google.maps.Geocoder();
        let infowindow = new google.maps.InfoWindow();
        let marker;
        
        eventInfo.forEach((event) => {
            geocoder.geocode({ address: event.location }, (results, status) => {
                if (status === "OK") {
                    marker = new google.maps.Marker({
                        map: map,
                        position: results[0].geometry.location,
                    });
                    google.maps.event.addListener(marker, 'click', function () {
                        infowindow.setContent('<p class="test">'+ event.name+ "</p>" +  event.time + '<br>' + event.location);
                        infowindow.open(map, this);
                    });
                }
            });
        });
        
    }
}

else if (currentPage === 'About Me') {
    function updateClock() {
        let date = new Date();
        let hour = date.getHours();
        let minute = date.getMinutes();
        let second = date.getSeconds();
        let am = "a.m.";
        if (hour > 12) {
            hour -= 12;
            am = "p.m.";
        }
        if (hour === 0) {
            hour = 12;

        }
        document.getElementById('hour').innerHTML = hour;
        document.getElementById('minute').innerHTML = minute;
        document.getElementById('second').innerHTML = second;
        document.getElementById('am').innerHTML = am;
        
    }
    updateClock();
    setInterval(updateClock, 1000);
}
else if (currentPage === 'Form') {
    let clear = document.getElementById('clear');
    function clearForm(){
        document.getElementById('event').value = '';
        document.getElementById('day').value = '';
        document.getElementById('start').value = '';
        document.getElementById('end').value = '';
        document.getElementById('phone').value = '';
        document.getElementById('location').value = '';
        document.getElementById('info').value = '';
        document.getElementById('url').innerHTML = '';
    }
    clear.addEventListener('click', clearForm);

    function initMap() {
        let map = new google.maps.Map(document.getElementById("form-map"), {
            center: { lat: 44.9727, lng: -93.23540000000003 },
            zoom: 15,
        });
        let geocoder = new google.maps.Geocoder();
        let input = document.getElementById("location");
        let autocomplete = new google.maps.places.Autocomplete(input);

        autocomplete.addListener('place_changed', () => {
            let place = autocomplete.getPlace();
            input.value = place.formatted_address;
        });

        map.addListener('click', (place) =>{
            geocoder.geocode({location: place.latLng}, (results, status) => {
                if (status === "OK") {
                    input.value = results[0].formatted_address;
                }
            });
        })
    }
}

