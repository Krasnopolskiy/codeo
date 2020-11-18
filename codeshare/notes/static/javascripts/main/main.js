$('#settings-btn').click(() => {
    if ($('#settings-drawer').css('transform') == 'matrix(1, 0, 0, 1, 420, 0)')
        $('#settings-drawer').css('transform', 'translateX(0)')
    else
        $('#settings-drawer').css('transform', 'translateX(420px)')
})

break_all = () => {
    error = true
    location = '/'
}

process_update_message = (body) => {
    data = JSON.parse(body.data)
    if (data['editor'] == Cookies.get('csrftoken'))
        return
    console.log(data)
    note.read = data['note']['read']
    note.edit = data['note']['edit']
    note.language = data['note']['language']
    editor.setValue(data['source'])
    editor.clearSelection()
}

create = (body = {}) => {
    api.create(body)
        .then(data => {
            console.log(data)
            if (data['message'] === 'created') {
                note.ismine = true
                note.read_link = url.origin + '/' + data['name']
                note.edit_link = url.origin + '/' + data['edit_link']
                window.history.replaceState('', '', note.read_link)
            }
            else break_all()
        })
}

retrieve = () => {
    api.retrieve()
        .then(data => {
            console.log(data)
            if (data['message'] === 'retrieved') {
                note.ismine = data['ismine']
                note.read_link = url.origin + '/' + note.name
                note.read = data['note']['read']
                note.edit = data['note']['edit']

                if (note.ismine)
                    note.edit_link = data['edit_link']

                note.language = data['note']['language']
                editor.setValue(data['source'])
                editor.setReadOnly(!note.ismine && !note.edit)
                editor.clearSelection()
                editor.session.setMode(note.language)

                if (note.ismine || note.edit)
                    $('#settings-btn').prop('disabled', false)
            }
            else break_all()
        })
}

update = (body, onclose = false) => {
    api.update(body, onclose)
}

$(document).ready(() => {
    if (note.name.length !== 0)
        retrieve()
})

$('#editor').click(() => {
    if (!note.edit) {
        if (note.name.length === 0)
            create()
    }
})

$('#editor').keyup(() => {
    if (note.edit || note.ismine) {
        setTimeout(update({
            'name': note.name,
            'source': editor.getValue(),
            'language': note.language,
            'edit': note.edit,
            'read': note.read
        }), 1000)
    }
})

$('#delete-btn').click(() => {
    api.delete().then(() => break_all())
})

$('#inputGroupSelectLanguage').change(() => {
    note.language = 'ace/mode/' + $('#inputGroupSelectLanguage').val()
    editor.session.setMode(note.language)
})