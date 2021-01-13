const url = new URL(window.location.href)
const editor = ace.edit('editor')
const client = uuid.v4()

editor.setOptions({
    showPrintMargin: false,
    readOnly: true,
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

let note = {
    'language': 'plain_text',
    'read': false,
    'edit': false,
    'source': ''
}

let ISMINE = false,
    READ_LINK = undefined,
    EDIT_LINK = undefined


if (url.pathname === '/') {
    $('#language-select').val('plain_text')
    $('#editor').click(() => $.post('/', {
        language: $('#language-select').val()
    }, (data) => {
        location.href = data['edit_link']
    }))
} else {
    let ws = new WebSocket('ws://' + url.host + url.pathname + '/' + client)
    ws.onmessage = (event) => {
        data = JSON.parse(event['data'])
        console.log(data)
        ISMINE = data['ismine']
        note['language'] = data['language']
        note['source'] = data['source']
        note['read'] = data['read']
        note['edit'] = data['edit']
        if (ISMINE) {
            READ_LINK = url.host + '/' + data['read_link']
            $('#read-settings .input-group input').val(READ_LINK)
            EDIT_LINK = url.host + '/' + data['edit_link']
            $('#edit-settings .input-group input').val(EDIT_LINK)
        }
        editor.setReadOnly(!ISMINE && !note['edit'] || url.pathname.length != 7)
        if (client !== data['client'])
            update_editor()
    }
    ws.onopen = () => {
        $('#editor').keyup(() => {
            note['source'] = editor.getValue()
            ws.send(JSON.stringify(note))
        })
    }
    $('#language-select').change(() => {
        note['language'] = $('#language-select').val()
        editor.session.setMode('ace/mode/' + note['language'])
        ws.send(JSON.stringify(note))
    })
    $('#read-settings .form-check input').click((event) => {
        note.read = event.target.checked
        ws.send(JSON.stringify(note))
    })
    $('#edit-settings .form-check input').click((event) => {
        note.edit = event.target.checked
        ws.send(JSON.stringify(note))
    })
    $('.fa-clipboard').click((event) => {
        $(event.target).parent().children('input').select()
        document.execCommand('copy')
        window.getSelection().removeAllRanges()
    })
}

update_editor = () => {
    $('#language-select').val(note['language'])
    editor.setValue(note['source'])
    editor.clearSelection()
    editor.navigateFileEnd()
    editor.focus()
    editor.session.setMode('ace/mode/' + note['language'])
}

let popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
let popoverList = popoverTriggerList.map((popoverTriggerEl) => {
    return new bootstrap.Popover(popoverTriggerEl)
})