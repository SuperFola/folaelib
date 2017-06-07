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

function create_modal(_id, _close_ID, text) {
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
    mod.appenChild = inter;
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











