class WebSocket {
    constructor(name, host) {
        this.name = [name, 'blank'][(name.length === 0) + 0]
        this.client = uuid.v4()
        this.host = host
    }

    connect = () => {
        this.websocket = new WebSocket(
            'ws://'
            + this.host
            + '/ws/note/update/'
            + this.name
            + '/'
            + this.client
        )
    }
}