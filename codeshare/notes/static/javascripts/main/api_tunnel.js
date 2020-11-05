class Api_tunnel {
    constructor(csrftoken, name) {
        this.csrftoken = csrftoken
        this.name = name
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
        let res = await fetch('/api/note/update', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrftoken
            },
            body: JSON.stringify(Object.assign({
                'name': this.name,
                'onclose': onclose
            }, body))
        })
        return await res.json()
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