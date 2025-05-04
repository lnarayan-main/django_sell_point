// ======= AJAX Setup for CSRF Token =========
function ajaxSetup() {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!(/^GET|HEAD|OPTIONS|TRACE$/i.test(settings.type))) {
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
                if (csrftoken) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        }
    });
}

// ======= Loader Show/Hide =========
function showLoader() {
    $('#global-loader').fadeIn();
}

function hideLoader() {
    $('#global-loader').fadeOut();
}

// ======= iziToast Notification Handler =========
function showToast(type, message) {
    iziToast[type]({
        title: type === 'success' ? 'Success' : 'Error',
        message: message,
        position: 'topRight',
        timeout: 3000
    });
}

// ======= Generalized AJAX Call =========
function ajaxCall({
    url = '',
    method = 'POST',
    data = {},
    contentType = 'application/x-www-form-urlencoded', // or 'application/json' or false for FormData
    processData = true,
    successCallback = function () {},
    errorCallback = function () {}
}) {
    showLoader();

    // Adjust contentType for JSON and FormData
    let finalData = data;
    if (contentType === 'application/json') {
        finalData = JSON.stringify(data);
    }

    $.ajax({
        url: url,
        method: method,
        data: finalData,
        contentType: contentType,
        processData: processData,
        success: function (response) {
            hideLoader();
            showToast('success', response.message || 'Success');
            successCallback(response);
        },
        error: function (xhr, status, error) {
            hideLoader();
            const errMsg = xhr.responseJSON?.message || 'Unexpected error occurred';
            showToast('error', errMsg);
            errorCallback(xhr.responseJSON || { status: 'error', message: errMsg });
        }
    });
}

// Call setup on page load
$(document).ready(function () {
    ajaxSetup();
});
