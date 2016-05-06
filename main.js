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

    var windowWidth = window.innerWidth;
    [].forEach.call(document.querySelectorAll(".parallax"), function(div) {
        var img = div.querySelector("img");

        function updateParallax(initial) {
            if(initial) {
                img.style.display = "block";
            }

            var containerHeight = div.offsetHeight;
            var scrollTop  = window.pageYOffset || document.documentElement.scrollTop;
            var rect = div.getBoundingClientRect();
            var top = rect.top + scrollTop;
            var bottom = top + containerHeight;
            var windowHeight = window.innerHeight;

            if ((bottom > scrollTop) && (top < (scrollTop + windowHeight))) {
                var imgHeight = img.offsetHeight;

                var parallaxDist = imgHeight - containerHeight;


                var windowBottom = scrollTop + windowHeight;
                var percentScrolled = (windowBottom - top) / (containerHeight + windowHeight);
                var parallax = Math.round((parallaxDist * percentScrolled));

                img.style.transform = "translate3D(-50%," + parallax + "px, 0)";
            }

        }

        updateParallax(true);
        window.addEventListener("scroll", function() { updateParallax(false); });
        window.addEventListener("resize", function() { updateParallax(false); });
    });

});
