class ApiTunnel {
    constructor(csrftoken, name, host) {
        this.csrftoken = csrftoken
        this.name = name
        this.websocket = new WebSocket('ws://' + host + '/ws/note/update')
    }

    create = async (body = {}) => {
        let res = await fetch('/api/note/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrftoken
            },
            body: JSON.stringify(body)
        })
        return await res.json()
    }

    retrieve = async () => {
        let res = await fetch('/api/note/retrieve/' + this.name, {
            method: 'GET',
            headers: { 'X-CSRFToken': this.csrftoken }
        })
        return await res.json()
    }

    update = async (body, onclose = false) => {
        this.websocket.send(JSON.stringify(body))
        this.websocket.onmessage = (event) => { console.log(event) }
    }

    delete = async () => {
        let res = await fetch('/api/note/delete', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrftoken
            },
            body: JSON.stringify({ "name": this.name })
        })
        return await res.json()
    }
}