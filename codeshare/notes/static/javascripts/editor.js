const url = new URL(window.location.href)
const notename = url.pathname.split('/')[1]
const editor = ace.edit("editor")

editor.setTheme("ace/theme/monokai")
editor.session.setTabSize(4)
editor.session.setUseSoftTabs(false);
editor.session.setMode("ace/mode/plain_text")


if (notename.length > 0) { retrieve() }
$('#editor').click(() => { if (url.pathname == '/') create() })
$('#editor').keyup(() => { update() })
$(window).on("beforeunload", () => { if (url.pathname != '/') update(true) })