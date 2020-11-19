class ApiTunnel {
    constructor(csrftoken, name, host) {
        this.csrftoken = csrftoken
        this.name = [name, 'blank'][(name.length === 0) + 0]
        this.client = uuid.v4()
        this.websocket = new WebSocket(
            'ws://'
            + host
            + '/ws/note/update/'
            + this.name
            + '/'
            + this.client
        )
    }

    create = async (body) => {
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

    update = async (body, onclose) => {
        this.websocket.send(JSON.stringify(body))
        this.websocket.onmessage = (event) => { process_update_message(event) }
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