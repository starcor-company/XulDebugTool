window.onload = function () {

    new QWebChannel(qt.webChannelTransport, function (channel) {
        window.bridge = channel.objects.bridge
    });

    var bObj = document.getElementsByClassName("html-attribute-value");
    for (var i = 0, item; item = bObj[i]; i++) {
        item.onclick = objclick;
    }

    function objclick() {
        window.bridge.strValue = this.innerText
    }
};
