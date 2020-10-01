class Api_tunnel {
    constructor(csrftoken) {
        this.csrftoken = csrftoken
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

    retrieve = async (notename) => {
        let res = await fetch('/api/note/retrieve/' + notename, {
            "method": "GET",
            "headers": { 'X-CSRFToken': this.csrftoken }
        })
        return await res.json()
    }

    update = async (notename, source, onclose = false) => {
        let res = await fetch('/api/note/update', {
            method: 'PUT',
            body: JSON.stringify({
                "name": notename,
                "source": source,
                "onclose": onclose
            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrftoken
            },
        })
        return await res.json()
    }
}