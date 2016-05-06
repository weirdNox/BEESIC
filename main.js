document.addEventListener("DOMContentLoaded", function() {
    var drawer = document.querySelector("#drawer");
    if(drawer != null) {
        obf = document.querySelector("#obfuscator");
        document.querySelector("#drawer-button").addEventListener("click", function() {
            drawer.classList.add("show");
            obf.classList.add("visible");
        });

        obf.addEventListener("click", function() {
            drawer.classList.remove("show");
            obf.classList.remove("visible");
        });
    }

    if(/iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream) {
        document.body.classList.add("ios");
        document.documentElement.classList.add("ios");
    }
});
