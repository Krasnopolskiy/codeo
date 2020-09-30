let create = () => {
    fetch('/api/note/create', {
        method: 'POST',
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data)
            if (data["message"] == "error") {
                loacation = '/'
                return
            }
            location = location + data.name
        })
}

let retrieve = () => {
    fetch('/api/note/retrieve/' + notename, {
        "method": "GET",
        "headers": {
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data)
            if (data["message"] == "error")
                location = '/'
            if (data["message"] == "retrieved") {
                note = data["note"]
                editor.setValue(data["source"])
                editor.session.setMode(note["language"])
                editor.clearSelection()
                editor.focus()
                editor.navigateFileEnd()
            }
        })
}


let update = (onclose = false) => {
    fetch('/api/note/update', {
        method: 'PUT',
        body: JSON.stringify({
            "name": notename,
            "source": editor.getValue(),
            "onclose": onclose
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': Cookies.get('csrftoken')
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data["message"] == "error")
                location = '/'
            console.log('Success:', data)
        })
}