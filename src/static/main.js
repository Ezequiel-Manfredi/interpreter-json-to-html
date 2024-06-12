let $form = document.querySelector("#form-file")
let $dropZone = document.querySelector("#drop-zone")
let $files = document.querySelector("#files")
let $console = document.querySelector("#console");
let $history = $console.querySelector("#history")
let $fileInputNav = document.querySelector(".input-nav")
let $fileInputContent = document.querySelector(".input-content")
let $submit = document.querySelector("#submit")
let $reset = document.querySelector('#reset')
let $fileOutputNav = document.querySelector(".output-nav")
let $fileOutputContent = document.querySelector(".output-content")

const eventDragAndDrop = ["dragover", "dragenter", "dragleave"]
let fileInputView = new InputView($fileInputNav, $fileInputContent)
let fileOutputView = new OutputView($fileOutputNav, $fileOutputContent)
const consoleHistoryView = new HistoryView($history)

// dos maneras de capturar archivos: drag and drop or input
eventDragAndDrop.forEach(nameEvent => {
    $dropZone.addEventListener(nameEvent, (e) => e.preventDefault())
})
$dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    checkFiles(e.dataTransfer.files)
})
$files.addEventListener("change", function () {
    checkFiles(this.files)
    $files.value = ''
})

// TODO: interaccion con la API
$submit.addEventListener("click", (e) => {
    fileInputView.fetchFilesParse()
        .then(outputFiles => outputFiles.forEach(
            (file, i) => fileOutputView.renderFile(file, i)
        ))
    e.target.classList.remove('active')
})

// reinicio de archivos
$reset.addEventListener("click", e => {
    $fileInputNav.innerHTML = ''
    $fileInputContent.innerHTML = ''
    $fileOutputNav.innerHTML = ''
    $fileOutputContent.innerHTML = ''
    fileInputView = new InputView($fileInputNav, $fileInputContent)
    fileOutputView = new OutputView($fileOutputNav, $fileOutputContent)
    $submit.classList.remove('active')
    $form.classList.remove("hidden")
})

// consola interactiva : interaccion con la API
$console.addEventListener("submit", async (e) => {
    e.preventDefault()
    let formData = new FormData(e.target)
    let stringToScan = formData.get("string-to-scan")

    consoleHistoryView.renderNewHistory(stringToScan)
    e.target.reset()
})

// verificar extension de archivos
const checkFiles = (fileList) => {
    let files = [...fileList]
    let isJson = files.every(f => f.type === "application/json")
    if (!isJson) {
        $dropZone.classList.add("shake")
        $dropZone.querySelector("p").innerHTML = "Solo se aceptan archivos .json"
        setTimeout(() => $dropZone.classList.remove("shake"), 800)
    } else {
        $form.classList.add("hidden")
        handlerFiles(files)
        $submit.classList.add("active")

    }
}

// obtener contenido de archivos y renderizado
const handlerFiles = async (files) => {
    let filesInputResults
    let filesPr = files.map(file => new Promise((res, rej) => {
        let reader = new FileReader()
        reader.onload = e => res({ name: file.name, content: e.target.result })
        reader.onerror = e => rej({ name: file.name, msj: e })
        reader.readAsText(file)
    }))
    try {
        filesInputResults = await Promise.all(filesPr)
    } catch (err) {
        console.error(err)
        return
    }
    filesInputResults.forEach((file, i) => fileInputView.renderFile(file, i))
}
