var currentTab = 0;
showTab(currentTab);

function showTab(n) {
    var x = document.getElementsByClassName("tab");
    x[n].style.display = "block";
    if (n == 0) {
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("prevBtn").style.display = "inline";
    }
    if (n == (x.length - 1)) {
        document.getElementById("nextBtn").innerHTML = "Mark Response";
        document.getElementById("nextBtn").addEventListener("click", submitForm);
    } else {
        document.getElementById("nextBtn").innerHTML = "Next";
        document.getElementById("nextBtn").removeEventListener("click", submitForm);
    }
    fixStepIndicator(n);
}

function nextPrev(n) {
    var x = document.getElementsByClassName("tab");
    if (n == 1 && !validateForm()) return false;
    x[currentTab].style.display = "none";
    currentTab = currentTab + n;
    showTab(currentTab);
}

function validateForm() {
    var x, y, i, valid = true;
    x = document.getElementsByClassName("tab");
    y = x[currentTab].getElementsByTagName("textarea");
    for (i = 0; i < y.length; i++) {
        if (y[i].value == "") {
            y[i].className += " invalid";
            valid = false;
        }
    }
    if (valid) {
        document.getElementsByClassName("step")[currentTab].className += " finish";
    }
    return valid;
}

function fixStepIndicator(n) {
    var i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
        x[i].className = x[i].className.replace(" active", "");
    }
    x[n].className += " active";
}

function submitForm() {
    var form = document.getElementById("regForm");
    var responseCard = document.getElementById("response-card");
    var loading = document.getElementById("loading");
    var success = document.getElementById("success");
    var error = document.getElementById("error");

    var xhr = new XMLHttpRequest();
    xhr.open("POST", form.action, true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    xhr.onload = function () {
        form.remove()
        responseCard.classList.add('show')
        loading.style.display = "none";
        if (xhr.status === 200) {
            success.style.display = "block";
            // Handle success response here
        } else {
            error.style.display = "block";
            // Handle error response here
        }
    };

    xhr.onerror = function () {
        loading.style.display = "none";
        error.style.display = "block";
        // Handle error response here
    };

    var formData = new FormData(form);
    var params = new URLSearchParams(formData).toString();

    xhr.send(params);
    loading.style.display = "block";
}

// Image Preview
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            var imagePreview = document.getElementById('imagePreview');
            imagePreview.style.backgroundImage = 'url(' + e.target.result + ')';
            imagePreview.style.display = 'none';
            fadeIn(imagePreview, 650);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function fadeIn(element, duration) {
    var op = 0;  // initial opacity
    var timer = setInterval(function () {
        if (op >= 1){
            clearInterval(timer);
        }
        element.style.display = 'block';
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op += op * 0.1 || 0.1;
    }, duration / 10);
}

var imageUpload = document.getElementById('imageUpload');
imageUpload.addEventListener('change', function() {
    readURL(this);
});
// End Image Preview