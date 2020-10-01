class Api_tunnel {
    constructor(csrftoken, notename, ismine = true) {
        this.csrftoken = csrftoken
        this.notename = notename
        this.ismine = ismine
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

    update = async (source, onclose = false) => {
        let res = await fetch('/api/note/update', {
            method: 'PUT',
            body: JSON.stringify({
                "name": this.notename,
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