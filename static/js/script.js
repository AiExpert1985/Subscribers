document.addEventListener('DOMContentLoaded', function(){
    load_page('subscribers');

});

function load_page(name){
    const request = new XMLHttpRequest();
    request.open('GET', `/${name}`);
    request.onload = () => {
        response_text = request.responseText
        response_json = JSON.parse(response_text);
        document.querySelector('#sub').innerHTML = response_text;
    };
    request.send();
}