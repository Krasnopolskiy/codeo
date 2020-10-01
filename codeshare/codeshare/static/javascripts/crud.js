class Api_tunnel {
    constructor(csrftoken) {
        this.csrftoken = csrftoken
        this.name = undefined
        this.source = undefined
    }

    create() {
        fetch('/api/note/create', {
            method: 'POST',
            headers: { 'X-CSRFToken': this.csrftoken }
        })
            .then(response => response.json())
            .then(data => { return data })
    }

    retrieve() {
        fetch('/api/note/retrieve/' + this.notename, {
            "method": "GET",
            "headers": { 'X-CSRFToken': this.csrftoken }
        })
            .then(response => response.json())
            .then(data => { return data })
    }

    update() {
        fetch('/api/note/update', {
            method: 'PUT',
            body: JSON.stringify({
                "name": this.notename,
                "source": this.source,
                "onclose": onclose
            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrftoken
            },
        })
            .then(response => response.json())
            .then(data => { return data })
    }
}


export { Api_tunnel }