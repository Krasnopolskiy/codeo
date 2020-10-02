const url = new URL(window.location.href)
const notename = url.pathname.split('/')[1]
const api = new Api_tunnel(Cookies.get('csrftoken'), notename)
const editor = ace.edit("editor")


editor.session.setMode("ace/mode/plain_text")
editor.setTheme("ace/theme/monokai")
editor.session.setUseSoftTabs(false)
editor.setShowPrintMargin(false)
editor.session.setTabSize(4)
editor.setReadOnly(true)
editor.setFontSize(18)


let error = false
let update = () => {
    if (!editor.getReadOnly())
        api.update({
            "source": editor.getValue(),
            "language": editor.session.getMode().$id,
            "published": $('#note_published')[0].checked,
            "protected": $('#note_protected')[0].checked
        })
            .then(data => {
                console.log(data)
                if (data["message"] == "error") {
                    error = true
                    location = url.origin
                }
            })
}


if (notename.length > 0) {
    api.retrieve()
        .then(data => {
            if (data["message"] == "retrieved") {
                editor.setValue(data.source)
                editor.session.setMode(data.note.language)
                $('#note_published')[0].checked = data.note.published
                $('#note_protected')[0].checked = data.note.protected
                editor.clearSelection()
                editor.navigateFileEnd()
                editor.focus()
                if (!data.ismine)
                    editor.setReadOnly(true)
                else
                    editor.setReadOnly(false)
                api.ismine = data.ismine
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

$('#editor').keyup(() => { update() })
$('#note_protected_btn').click(() => {
    $('#note_protected')[0].checked = !$('#note_protected')[0].checked
    update()
})
$('#note_published_btn').click(() => {
    $('#note_published')[0].checked = !$('#note_published')[0].checked
    update()
})

$(window).on("beforeunload", () => {
    if (api.ismine && !editor.getReadOnly() && !error)
        api.update({ "source": editor.getValue() }, true)
            .then(data => {
                console.log(data)
            })
})
