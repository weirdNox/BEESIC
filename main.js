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
});
