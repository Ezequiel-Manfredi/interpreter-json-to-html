class OutputView extends FileView {
  constructor($fileNav, $fileContent) {
    super($fileNav, $fileContent)
  }

  createContent(content, i) {
    let $pre = super.createContent(content, i)
    let $download = document.createElement('a')
    $download.classList.add('download')
    let fileInfo = this.filesInfo[i]

    let file = new Blob([fileInfo.raw], { type: "text/html" })
    let url = URL.createObjectURL(file)
    $download.href = url
    $download.setAttribute('download', fileInfo.name)
    $download.innerHTML = 'Descargar'

    $pre.append($download)
  }
}