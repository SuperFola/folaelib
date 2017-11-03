var getCookies = function() {
    var pairs = document.cookie.split(";");
    var cookies = {};
    for (var i=0; i < pairs.length; i++) {
        var pair = pairs[i].split("=");
        cookies[pair[0]] = unescape(pair[1]);
    }
    return cookies;
}

function qsd(type) {
    return document.createElement(type);
}

function dce(id) {
    return document.getElementById(id);
}

function extractUrlParams() {
    var t = location.search.substring(1).split('&'),
        f = [];
    for (var i = 0; i < t.length; i++) {
        var x = t[i].split('=');
        f[x[0]] = x[1];
    }
    return f;
}

function load_script(script_name, onload)  {
    var script = qsd("script");
    script.src = script_name+".js"
    script.type = "text/javascript";
    script.onload = onload;
    document.head.appendChild(script);
}

function create_modal(_id, text) {
    var mod = qsd("div");
    mod.id = _id;
    mod.className = "modal";
        var inter = qsd("div");
        inter.className = "modal-content";
            var span = qsd("span");
            span.className = "close";
            span.innerHTML = "&times;";
            //----
            var content = qsd("p");
            content.textContent = text;
        inter.appendChild(span);
        inter.appendChild(content);
    //----
    on(span, "click", function () {
        mod.style.display = "none";
    });
    on(window, "click", function() {
        mod.style.display = "none";
    });
    //----
    mod.appendChild = inter;
    document.body.appendChild(mod);
}

function show_modal(name) {
    dce(name).style.display = 'block';
}

var on = (function() {
    if (window.addEventListener) {
        return function(target, type, listener) {
            target.addEventListener(type, listener, false);
        };
    }
    else {
        return function(object, sEvent, fpNotify) {
            object.attachEvent("on" + sEvent, fpNotify);
        };
    }
}());

function delete_discord_messages(auth) {
    const authToken = auth;
    const channel = window.location.href.split('/').pop();
    const baseURL = `https://discordapp.com/api/channels/${channel}/messages`;
    const headers = {"Authorization": authToken};

    let clock = 0;
    let interval = 500;

    function delay(duration) {
        return new Promise((resolve, reject) => {
            setTimeout(() => resolve(), duration);
        });
    }

    fetch(baseURL + '?limit=100', {headers})
        .then(resp => resp.json())
        .then(messages => {
        return Promise.all(messages.map((message) => {
            return delay(clock += interval).then(() => fetch(`${baseURL}/${message.id}`, {headers, method: 'DELETE'}));
        }));
    }).then(() => console.log("Done!"));
}

function stars() {
    if (!window.requestAnimationFrame) {
        window.requestAnimationFrame = (window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.msRequestAnimationFrame || window.oRequestAnimationFrame || function (callback) {
            return window.setTimeout(callback, 1000 / 60);
        });
    }

    (function ($, window) {
        /**
         * Makes a nice constellation on canvas
         * @constructor Constellation
         */
        function Constellation (canvas, options) {
            var $canvas = $(canvas),
                context = canvas.getContext('2d'),
                defaults = {
                    star: {
                        color: 'rgba(255, 255, 255, .5)',
                        width: 1,
                        randomWidth: true
                    },
                    line: {
                        color: 'rgba(255, 255, 255, .5)',
                        width: 0.2
                    },
                    position: {
                        x: 0, // This value will be overwritten at startup
                        y: 0 // This value will be overwritten at startup
                    },
                    width: window.innerWidth,
                    height: window.innerHeight,
                    velocity: 0.1,
                    length: 100,
                    distance: 120,
                    radius: 150,
                    stars: []
                },
                config = $.extend(true, {}, defaults, options);

            function Star () {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.vx = (config.velocity - (Math.random() * 0.5));
                this.vy = (config.velocity - (Math.random() * 0.5));
                this.radius = config.star.randomWidth ? (Math.random() * config.star.width) : config.star.width;
            }

            Star.prototype = {
                create: function(){
                    context.beginPath();
                    context.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
                    context.fill();
                },

                animate: function(){
                    var i;
                    for (i = 0; i < config.length; i++) {
                        var star = config.stars[i];
                        if (star.y < 0 || star.y > canvas.height) {
                            star.vx = star.vx;
                            star.vy = - star.vy;
                        } else if (star.x < 0 || star.x > canvas.width) {
                            star.vx = - star.vx;
                            star.vy = star.vy;
                        }
                        star.x += star.vx;
                        star.y += star.vy;
                    }
                },

                line: function(){
                    var length = config.length, iStar, jStar, i, j;

                    for (i = 0; i < length; i++) {
                        for (j = 0; j < length; j++) {
                            iStar = config.stars[i];
                            jStar = config.stars[j];

                            if (
                                (iStar.x - jStar.x) < config.distance &&
                                (iStar.y - jStar.y) < config.distance &&
                                (iStar.x - jStar.x) > - config.distance &&
                                (iStar.y - jStar.y) > - config.distance
                            ) {
                                if (
                                    (iStar.x - config.position.x) < config.radius &&
                                    (iStar.y - config.position.y) < config.radius &&
                                    (iStar.x - config.position.x) > - config.radius &&
                                    (iStar.y - config.position.y) > - config.radius
                                ) {
                                    context.beginPath();
                                    context.moveTo(iStar.x, iStar.y);
                                    context.lineTo(jStar.x, jStar.y);
                                    context.stroke();
                                    context.closePath();
                                }
                            }
                        }
                    }
                }
            };

            this.createStars = function () {
                var length = config.length,
                    star,
                    i;
                context.clearRect(0, 0, canvas.width, canvas.height);
                for (i = 0; i < length; i++) {
                    config.stars.push(new Star());
                    star = config.stars[i];
                    star.create();
                }
                star.line();
                star.animate();
            };

            this.setCanvas = function () {
                canvas.width = config.width;
                canvas.height = config.height;
            };

            this.setContext = function () {
                context.fillStyle = config.star.color;
                context.strokeStyle = config.line.color;
                context.lineWidth = config.line.width;
            };

            this.setInitialPosition = function () {
                if (!options || !options.hasOwnProperty('position')) {
                    config.position = {
                        x: canvas.width * 0.5,
                        y: canvas.height * 0.5
                    };
                }
            };

            this.loop = function (callback) {
                callback();
                window.requestAnimationFrame(function () {this.loop(callback);}.bind(this));
            };

            this.bind = function () {
                $canvas.on('mousemove', function(e){
                    config.position.x = e.pageX - $canvas.offset().left;
                    config.position.y = e.pageY - $canvas.offset().top;
                });
            };

            this.init = function () {
                this.setCanvas();
                this.setContext();
                this.setInitialPosition();
                this.loop(this.createStars);
                this.bind();
            };
        }

        $.fn.constellation = function (options) {
            return this.each(function () {
                var c = new Constellation(this, options);
                c.init();
            });
        };
    })($, window);

    // Init plugin
    $('canvas').constellation({
        star: {width: 3},
        line: {color: 'rgba(255, 255, 255, .5)'},
        radius: 250
    });
}






