document.addEventListener('DOMContentLoaded', function(){

    submit_button = document.querySelector('#submit-button')
    user_message = document.querySelector('#user-message')
    browser_label = document.querySelector('#browser-label')
    loading_img = document.querySelector('#loading-img')
    submit_button.disabled = true;
    loading_img.style.display = "none";

    const fileSelector = document.querySelector('#customFile')
    fileSelector.addEventListener('change', () => {
        user_message.innerHTML = " &#x2714; تم اختيار الملفات"
        submit_button.disabled = false;
        browser_label.innerHTML = " ";
    });

    submit_button.onclick = function() {
        document.querySelector('#submit-button').disabled = true;
        user_message.innerHTML = "جاري معالجة البيانات";
        loading_img.style.display = "inline";
    }
});


