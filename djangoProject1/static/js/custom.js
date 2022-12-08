let autocomplete;

function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            componentRestrictions: {'country': ['ua']},
        })
    autocomplete.addEventListener('place_changed', onPlaceChanged);
}
function onPlaceChanged () {
    var place = autocomplete.getPlace();
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing..."
    }
    else{
        console.log('place name=>', place.name)
    }
}