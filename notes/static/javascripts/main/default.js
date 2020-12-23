const url = new URL(window.location.href)

let note = {
    name: url.pathname.split('/')[1],
    ismine: false,
    read: false,
    read_link: '',
    edit: false,
    edit_link: '',
    language: 'ace/mode/plain_text'
}

const api = new ApiTunnel(Cookies.get('csrftoken'), note.name, url.host)
const editor = ace.edit('editor')

let error = false

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

$('#settings-btn').prop('disabled', true)