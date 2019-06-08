
DJANGO_STATIC_URL = '{{ entry/images/Rocket.jpg }}';

function updateImage(elementID, url) {
    document.getElementById(elementID).src = url;
}