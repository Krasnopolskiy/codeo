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

update_setting_btns = () => {
    if (note.read) {
        $('#read-link-input')[0].value = note.read_link
        $('#allow-reading-btn').css('display', 'none')
        $('#disallow-reading-btn').css('display', 'block')
    } else {
        $('#read-link-input')[0].value = ''
        $('#allow-reading-btn').css('display', 'block')
        $('#disallow-reading-btn').css('display', 'none')
    }
    if (note.edit) {
        $('#edit-link-input')[0].value = note.edit_link
        $('#allow-editing-btn').css('display', 'none')
        $('#disallow-editing-btn').css('display', 'block')
    } else {
        $('#edit-link-input')[0].value = ''
        $('#allow-editing-btn').css('display', 'block')
        $('#disallow-editing-btn').css('display', 'none')
    }
}

process_update_message = (event) => {
    data = JSON.parse(JSON.parse(event['data']).message)
    note.read = data['note']['read']
    note.edit = data['note']['edit']
    update_setting_btns()
    if (data['client'] === api.client)
        return
    note.language = data['note']['language']
    editor.setValue(data['source'])
    editor.clearSelection()
    editor.focus()
    editor.navigateFileEnd()
}

create = (body = {}) => {
    api.create(body)
        .then(data => {
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
            if (data['message'] === 'retrieved') {
                note.ismine = data['ismine']
                note.read_link = url.origin + '/' + note.name
                note.read = data['note']['read']
                note.edit = data['note']['edit']

                if (note.ismine)
                    note.edit_link = url.origin + '/' + data['edit_link']

                note.language = data['note']['language']
                editor.setValue(data['source'])
                editor.setReadOnly(!note.ismine && !note.edit)
                editor.clearSelection()
                editor.session.setMode(note.language)
                editor.focus()
                editor.navigateFileEnd()

                if (note.ismine || note.edit)
                    $('#settings-btn').prop('disabled', false)

                update_setting_btns()
            }
            else break_all()
        })
}

update = (onclose = false) => {
    api.update({
        'name': note.name,
        'source': editor.getValue(),
        'language': note.language,
        'edit': note.edit,
        'read': note.read
    }, onclose)
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
    if (note.edit || note.ismine)
        update()
})

$('#allow-reading-btn').click(() => {
    note.read = true
    update()
})

$('#disallow-reading-btn').click(() => {
    note.read = false
    note.edit = false
    update()
})

$('#allow-editing-btn').click(() => {
    note.read = true
    note.edit = true
    update()
})

$('#disallow-editing-btn').click(() => {
    note.edit = false
    update()
})

$('#delete-btn').click(() => {
    api.delete().then(() => break_all())
})

$('#inputGroupSelectLanguage').change(() => {
    note.language = 'ace/mode/' + $('#inputGroupSelectLanguage').val()
    editor.session.setMode(note.language)
})