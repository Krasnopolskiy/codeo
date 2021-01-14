const url = new URL(window.location.href)
const editor = ace.edit('editor')
const client = uuid.v4()


let error = init_data === 'undefined'
let note, ws, ismine, read_link, edit_link
if (!error)
{
    init_data = JSON.parse(init_data)
    note = init_data['editable']
    ismine = init_data['ismine']
    read_link = url.host + '/' + init_data['read_link']
    edit_link = url.host + '/' + init_data['edit_link']
    $('#read-settings .input-group input').val(read_link)
    $('#edit-settings .input-group input').val(edit_link)
}


editor.setOptions({
    showPrintMargin: false,
    readOnly: error || !ismine && (!note['edit'] || url.pathname.length != 7),
    fontSize: 18,
    theme: 'ace/theme/monokai'
})
editor.session.setOptions({
    tabSize: 4,
    useSoftTabs: true,
    mode: 'ace/mode/plain_text',
    useWorker: false
})


$.ajaxSetup({
    headers: {
        'X-CSRFToken': $.cookie('csrftoken')
    }
})


if (url.pathname === '/') {
    $('#language-select').val('plain_text')
    $('#editor').click(() => $.post('/', {
        language: $('#language-select').val()
    }, (data) => {
        document.location += data['redirect']
    }))
} else {
    if (error)
        document.location = '/'

    ws = new WebSocket('ws://' + url.host + url.pathname + '/' + client)

    ws.onmessage = (event) => {
        data = JSON.parse(event['data'])
        console.log(data)
        note = data['editable']
        if (client !== data['client'])
            update_editor()
    }

    $('#editor').keyup(() => request_update())
    $('#language-select').change(() => request_update())
    $('#read-settings .form-check input').click(() => request_update())
    $('#edit-settings .form-check input').click(() => request_update())
}

request_update = () => {
    note['language'] = $('#language-select').val()
    note['read'] = $('#read-settings .form-check input').is(':checked')
    note['edit'] = $('#edit-settings .form-check input').is(':checked')
    note['source'] = editor.getValue()
    editor.session.setMode('ace/mode/' + note['language'])
    ws.send(JSON.stringify(note))
}

update_editor = () => {
    $('#language-select').val(note['language'])
    editor.setValue(note['source'])
    editor.clearSelection()
    editor.navigateFileEnd()
    editor.focus()
    editor.session.setMode('ace/mode/' + note['language'])
}