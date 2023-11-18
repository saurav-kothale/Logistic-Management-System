function loadContent(url) {
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            document.getElementsByClassName('main-container').innerHTML = xhr.responseText;
        }
    };

    xhr.open('GET', url, true);
    xhr.send();
}



