const url = new URL(window.location.href)
const notename = url.pathname.split('/')[1]
const api = new Api_tunnel(Cookies.get('csrftoken'), notename)
const editor = ace.edit("editor")

editor.setOptions({
    showPrintMargin: false,
    readOnly: true,
    fontSize: 18,
    theme: "ace/theme/monokai"
})
editor.session.setOptions({
    tabSize: 4,
    useSoftTabs: true,
    mode: "ace/mode/plain_text"
})
editor.$enableAutoIndent


let error = false


let update = () => {
    console.log(editor.session.getMode().$id)
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

$('#note_protect_btn').click(() => {
    if (!editor.getReadOnly())
        $('#note_protected')[0].checked = !$('#note_protected')[0].checked
    update()
})

$('#note_publish_btn').click(() => {
    if (!editor.getReadOnly())
        $('#note_published')[0].checked = !$('#note_published')[0].checked
    update()
})

$('#note_delete_btn').click(() => {
    api.delete()
        .then(data => {
            console.log(data)
            if (data["message"] == "deleted")
                location = url.origin
        })
})

$(window).on('beforeunload', () => {
    if (api.ismine && !editor.getReadOnly() && !error)
        api.update({ "source": editor.getValue() }, true)
            .then(data => {
                console.log(data)
            })
})

$(document).ready(() => {
    $('.language-item').click(el => {
        editor.session.setMode("ace/mode/" + el.currentTarget.innerText.toLowerCase())
        setTimeout(() => { update() }, 1000)
    })
})