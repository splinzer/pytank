function worker_function() {
    // 用于记录战斗指令序列，用于回放战斗
    game_record = [];
    //自动连接websocket服务器
    doConnect();
    // 接收浏览器前台消息
    self.onmessage = function (evt) {
        // 当接收到relay消息启动战斗回放
        if (evt.data == 'replay') {
            replay();
        }
    }

    function doConnect() {
        websocket = new WebSocket("ws://localhost:8000/");
        websocket.onopen = function (evt) {
            onWebsocketOpen(evt);
        };
        websocket.onclose = function (evt) {
            onWebsocketClose(evt);
        };
        websocket.onmessage = function (evt) {
            onWebsocketMessage(evt);
        };
        websocket.onerror = function (evt) {
            onWebsocketError(evt);
        };
    }

    function onWebsocketOpen(evt) {

    }

    function onWebsocketClose(evt) {

    }

    function onWebsocketMessage(evt) {
        // writeToScreen(evt.data + '\n');
        console.log(evt.data);
        var data = decoder(evt.data);
        //将获取到的战场信息发给前台浏览器
        postMessage(data);
        // 保存战斗录像
        game_record.push(data);
    }

    function onWebsocketError(evt) {
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

    // 该函数用于回放战斗录像
    function replay() {
        i = 0;

        function next_commnad() {
            if (i < game_record.length) {
                postMessage(game_record[i]);
            }
            else {
                clearInterval(s)
            }
            i++;
        }

        s = setInterval(next_commnad, 100);
    }
}

// This is in case of normal worker start
// "window" is not defined in web worker
// so if you load this file directly using `new Worker`
// the worker code will still execute properly
if (window != self)
    worker_function();





