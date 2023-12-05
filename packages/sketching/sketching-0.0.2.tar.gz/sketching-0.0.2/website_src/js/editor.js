function main() {
    const editor = initEditor();
    addEventListeners(editor);

    window.addEventListener("error", (error) => {
        const display = document.getElementById("runtime-error-display");
        const escaped = new Option(error.message).innerHTML;
        display.innerHTML = escaped;
        display.style.display = "block";
    });

    showLoaded();
}


function initEditor() {
    const editor = ace.edit("editor");
    editor.getSession().setMode("ace/mode/python");
    return editor;
}


function runProgram(editor) {
    showLoading();

    const exampleCanvas = document.querySelector(".example-canvas");

    const idPieces = exampleCanvas.id.split("-");
    const idNum = parseInt(idPieces[2]) + 1;
    const newId = idPieces[0] + "-" + idPieces[1] + "-" + idNum;

    exampleCanvas.id = newId;

    const rawCode = editor.getValue();
    const outputCode = rawCode.replaceAll("\"example-canvas\"", "\"" + newId + "\"")
        .replaceAll("\'example-canvas\'", "\'" + newId + "\'");

    const wrappedCode = "<py-script id='code-tag'>\n" + outputCode + "\n</py-script>";
    document.getElementById("main-script").innerHTML = wrappedCode;

    document.querySelectorAll(".py-error").forEach((x) => x.remove());
    document.getElementById("runtime-error-display").style.display = "none";

    setTimeout(() => {
        showLoaded();
        document.getElementById(newId).scrollIntoView();
    }, 500);
}


function addEventListeners(editor) {
    document.getElementById("run-button").addEventListener("click", () => runProgram(editor));
}


function showLoading() {
    document.getElementById("loading-msg").style.display = "inline-block";
    document.getElementById("loaded-msg").style.display = "none";
}


function showLoaded() {
    document.getElementById("loading-msg").style.display = "none";
    document.getElementById("loaded-msg").style.display = "inline-block";
}


main();