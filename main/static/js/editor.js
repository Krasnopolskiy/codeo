const editor = ace.edit('editor')
const client = uuid.v4()


let url = new URL(window.location.href)
let error = init_data === undefined
let note, ws, ismine, read_link, edit_link


init_note = (init_data) => {
    error = false
    note = init_data['editable']
    ismine = init_data['ismine']
    read_link = url.host + '/' + init_data['read_link']
    edit_link = url.host + '/' + init_data['edit_link']
    $('#editor').off('click')
    $('#settings-btn').prop('disabled', !ismine)
    $('#delete-btn').attr('href', 'delete/' + init_data['id'] + '?next=/')
    $('#read-settings .input-group input').val(read_link)
    $('#edit-settings .input-group input').val(edit_link)
}

init_websocket = () => {
    ws = new WebSocket('ws://' + url.host + url.pathname + '/' + client)

    ws.onmessage = (event) => {
        data = JSON.parse(event['data'])
        note = data['editable']
        if (client !== data['client'])
            update_editor()
    }

    $('#editor').keyup(() => request_update())
    $('#language-select').change(() => request_update())
    $('#read-settings .form-check input').click(() => request_update())
    $('#edit-settings .form-check input').click(() => request_update())
    $('#name-settings .input-group button').click(() => {
        request_update()
        document.title = note['name'] + ' - codeo'
    })
}

request_update = () => {
    note['name'] = $('#name-settings .input-group input').val()
    note['read'] = $('#read-settings .form-check input').prop('checked')
    note['edit'] = $('#edit-settings .form-check input').prop('checked')
    note['source'] = btoa(editor.getValue())
    note['language'] = $('#language-select').val()
    editor.session.setMode('ace/mode/' + note['language'])
    ws.send(JSON.stringify(note))
}

update_editor = () => {
    document.title = note['name'] + ' - codeo'
    $('#name-settings .input-group input').val(note['name'])
    $('#language-select').val(note['language'])
    $('#read-settings .form-check input').prop('checked', note['read'])
    $('#edit-settings .form-check input').prop('checked', note['edit'])
    editor.setValue(atob(note['source']))
    editor.setReadOnly(error || !ismine && (!note['edit'] || url.pathname.length != 7))
    editor.clearSelection()
    editor.navigateFileEnd()
    editor.focus()
    editor.session.setMode('ace/mode/' + note['language'])
}


editor.setOptions({
    showPrintMargin: false,
    readOnly: false,
    scrollPastEnd: 1,
    fontSize: 16,
    fontFamily: 'MesloLGS',
    theme: 'ace/theme/monokai',
    enableBasicAutocompletion: true,
    fixedWidthGutter: true,
    enableLiveAutocompletion: true,
    enableSnippets: true
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
$('#language-select').val('plain_text')


$('#editor').click(() => {
    $.post('/', {
        language: $('#language-select').val()
    }, (data) => {
        init_data = data['init_data']
        window.history.pushState({}, '', init_data['read_link'])
        url = new URL(window.location.href)
        init_note(init_data)
        init_websocket()
        update_editor()
    })
})

if (url.pathname !== '/') {
    init_note(init_data)
    init_websocket()
    update_editor()
}