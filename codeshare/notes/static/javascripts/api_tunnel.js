class Api_tunnel {
    constructor(csrftoken, notename) {
        this.csrftoken = csrftoken
        this.notename = notename
    }

    create = async (body = {}) => {
        let res = await fetch('/api/note/create', {
            method: 'POST',
            body: JSON.stringify(body),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrftoken
            }
        })
        return await res.json()
    }

    retrieve = async () => {
        let res = await fetch('/api/note/retrieve/' + this.notename, {
            "method": "GET",
            "headers": { 'X-CSRFToken': this.csrftoken }
        })
        return await res.json()
    }

    update = async (body, onclose = false) => {
        let res = await fetch('/api/note/update', {
            method: 'PUT',
            body: JSON.stringify(Object.assign({
                "name": this.notename,
                "onclose": onclose
            }, body)),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrftoken
            },
        })
        return await res.json()
    }

    delete = async () => {
        let res = await fetch('/api/note/delete', {
            method: 'DELETE',
            body: JSON.stringify({ "name": this.notename }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrftoken
            },
        })
        return await res.json()
    }
}