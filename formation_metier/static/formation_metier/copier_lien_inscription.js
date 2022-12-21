function CopierText() {
    let text = document.getElementById('lien_inscription').innerText
    navigator.clipboard.writeText(text)
}