window.onload = function () {

    new QWebChannel(qt.webChannelTransport, function (channel) {
        window.bridge = channel.objects.bridge
    });

    var bObj = document.getElementsByClassName("html-attribute");
    for (var i = 0, item; item = bObj[i]; i++) {
        if (item.children[0].innerText == "id") {
            item.onclick = objclick;
        }
    }

    function objclick() {
        var id = this.children[1].innerText
        var xml = document.getElementById("webkit-xml-viewer-source-xml").innerHTML
        window.bridge.strValue = JSON.stringify({"Id":id,"xml":xml});
    }

    // function findParentByClass(node,clazzName) {
    //     var parentNode = node.parentNode;
    //     while (parentNode){
    //         if(parentNode.getAttribute("class") == clazzName){
    //             return parentNode;
    //         }
    //         parentNode = parentNode.parentNode;
    //     }
    // }
};
