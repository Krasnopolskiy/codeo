const url = new URL(window.location.href)

let note = {
    name: url.pathname.split('/')[1],
    language: 'ace/mode/plain_text'
}

const websocket = new WebSocket(note.name, url.host)
const editor = ace.edit('editor')

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
    headers: { 'X-CSRFToken': $.cookie('csrftoken') }
})

$('#editor').click(() => {
    $.post('/', (data) => {
        console.log(data)
    })
})