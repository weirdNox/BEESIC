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

    function detectIe() {
        var ua = window.navigator.userAgent;

        var msie = ua.indexOf('MSIE ');
        if (msie > 0) {
            return parseInt(ua.substring(msie + 5, ua.indexOf('.', msie)), 10);
        }

        var trident = ua.indexOf('Trident/');
        if (trident > 0) {
            var rv = ua.indexOf('rv:');
            return parseInt(ua.substring(rv + 3, ua.indexOf('.', rv)), 10);
        }

        var edge = ua.indexOf('Edge/');
        if (edge > 0) {
            return parseInt(ua.substring(edge + 5, ua.indexOf('.', edge)), 10);
        }

        return false;
    }

    var lastScroll = 0;
    var ticking = false;
    var images = document.querySelectorAll(".parallax img");
    var pageHeight = Math.max(document.body.scrollHeight, document.body.offsetHeight,
                              document.documentElement.clientHeight, document.documentElement.scrollHeight,
                              document.documentElement.offsetHeight);
    var windowHeight = window.innerHeight;

    function parallax(img, scroll, first) {
        if(first) {
            img.style.display = "block";
        }
        scroll = Math.max(0, Math.min(pageHeight - windowHeight, scroll));
        var div = img.parentElement;

        img.style.top = "0";

        var containerHeight = div.offsetHeight;
        var rect = div.getBoundingClientRect();
        var top = rect.top + scroll;
        var bottom = top + containerHeight;

        if ((bottom > scroll) && (top < (scroll + windowHeight))) {
            var imgHeight = img.offsetHeight;

            var parallaxDist = imgHeight - containerHeight;

            var windowBottom = scroll + windowHeight;
            var percentScrolled = (windowBottom - top) / (containerHeight + windowHeight);
            var parallax = Math.round((parallaxDist * percentScrolled));

            img.style.transform = "translate3D(-50%," + (containerHeight + parallax - imgHeight) + "px, 0)";
        }
    }

    function requestParallax() {
        lastScroll = window.scrollY;
        if (!ticking) {
            ticking = true;
            window.requestAnimationFrame(function() {
                for(i = 0; i < images.length; ++i) {
                    parallax(images[i], lastScroll, false);
                }
                ticking = false;
            });
        }
    }

    if(!detectIe())
    {
        window.addEventListener('scroll', requestParallax);
        window.addEventListener('resize', requestParallax);

        for (i = 0; i < images.length; ++i) {
            var img = images[i];
            img.addEventListener('load', function() {
                parallax(this, window.scrollY, true);
            });
            if(img.complete) parallax(img, window.scrollY, true);
        }
    }
});
