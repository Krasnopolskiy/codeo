const url = new URL(window.location.href)
const notename = url.pathname.split('/')[1]
const api = new Api_tunnel(Cookies.get('csrftoken'))
const editor = ace.edit("editor")


editor.session.setMode("ace/mode/plain_text")
editor.setTheme("ace/theme/monokai")
editor.session.setUseSoftTabs(false)
editor.session.setTabSize(4)
editor.setReadOnly(true)


let error = false


if (notename.length > 0) {
    api.retrieve(notename)
        .then(data => {
            if (data["message"] == "retrieved") {
                editor.setValue(data.source)
                editor.session.setMode(data.note.language)
                editor.clearSelection()
                editor.navigateFileEnd()
                editor.focus()
                if (!data["ismine"])
                    editor.setReadOnly(true)
                else
                    editor.setReadOnly(false)
                api.ismine = data["ismine"]
            } else {
                error = true
                location = url.origin
            }
        })
}

$('#editor').click(() => {
    if (editor.getReadOnly()) {
        let body = {}
        if (url.pathname != '/')
            body = {
                "source": editor.getValue(),
                "language": editor.session.getMode().$id
            }
        api.create(body)
            .then(data => {
                if (data["message"] == "created")
                    location = url.origin + '/' + data["notename"]
            })
    }
})

$('#editor').keyup(() => {
    if (!editor.getReadOnly())
        api.update(notename, editor.getValue())
            .then(data => {
                console.log(data)
                if (data["message"] == "error") {
                    error = true
                    location = url.origin
                }
            })
})

$(window).on("beforeunload", () => {
    if (api.ismine && !editor.getReadOnly() && !error)
        api.update(notename, editor.getValue(), true)
            .then(data => {
                console.log(data)
            })
})
