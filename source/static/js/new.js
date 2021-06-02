let g_preview_flag = false;
let g_preview = document.getElementById('preview');
let g_previewpane = document.getElementById('previewpane');
let g_body = document.getElementById('body');

g_body.addEventListener('keyup', onInputChange, false);

function onTogglePreview(o) {
    if (o.checked) {
        g_previewpane.classList.remove('d-none');
        g_preview_flag = true;
        onInputChange();
    } else {
        g_previewpane.classList.add('d-none');
        g_preview_flag = false;
    }
}

function onInputChange() {
    if (g_preview_flag) {
        g_preview.contentDocument.body.innerHTML = marked(g_body.value);
    }
}