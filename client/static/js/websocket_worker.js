function worker_function() {
    // all code here
    //自动连接websocket服务器
    doConnect();


    function doConnect() {
        websocket = new WebSocket("ws://localhost:8000/");
        websocket.onopen = function (evt) {
            onOpen(evt);
        };
        websocket.onclose = function (evt) {
            onClose(evt);
        };
        websocket.onmessage = function (evt) {
            onMessage(evt);
        };
        websocket.onerror = function (evt) {
            onError(evt);
        };
    }

    function onOpen(evt) {

    }

    function onClose(evt) {

    }

    function onMessage(evt) {
        // writeToScreen(evt.data + '\n');
        console.log(evt.data);
        var data = decoder(evt.data);
        //将获取到的战场信息发给前台浏览器
        postMessage(data);
    }

    function onError(evt) {
        // writeToScreen('error: ' + evt.data + '\n');
        console.log('error: ' + evt.data)
        websocket.close();
    }

    /*websocket消息解码器
    raw消息如下：
    id:t1|width:20|height:20|x:95|y:50|direction:3|velocity:5|life:100|oil:100|weapon:0|status:3;
    id:t2|width:20|height:20|x:255|y:50|direction:2|velocity:5|life:100|oil:100|weapon:0|status:3
     */
    function decoder(str) {
        var target = []
        var groups = str.split(';')
        for (i = 0; i < groups.length; i++) {
            var list = groups[i].split('|')
            var row = {}
            for (j = 0; j < list.length; j++) {
                var pair = list[j].split(':')
                row[pair[0]] = pair[1]
            }
            target.push(row)
        }
        return target
    }
}

// This is in case of normal worker start
// "window" is not defined in web worker
// so if you load this file directly using `new Worker`
// the worker code will still execute properly
if (window != self)
    worker_function();




