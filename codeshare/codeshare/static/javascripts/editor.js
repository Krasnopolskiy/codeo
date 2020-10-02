import Api_tunnel from './crud'

const url = new URL(window.location.href)
const notename = url.pathname.split('/')[1]
const editor = ace.edit("editor")
const api = new Api_tunnel(Cookies.get('csrftoken'))

editor.setTheme("ace/theme/monokai")
editor.session.setTabSize(4)
editor.session.setUseSoftTabs(false);
editor.session.setMode("ace/mode/plain_text")

console.log(api)


// if (notename.length > 0) { retrieve(csrftoken, notename) }
// $('#editor').click(() => { if (url.pathname == '/') create(csrftoken) })
// $('#editor').keyup(() => { update(csrftoken, notename, editor.getValue()) })
// $(window).on("beforeunload", () => { if ((url.pathname != '/') && !error) update(csrftoken, notename, editor.getValue(), true) })