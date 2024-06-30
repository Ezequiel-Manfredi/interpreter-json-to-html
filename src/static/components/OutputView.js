class OutputView extends FileView {
  constructor($fileNav, $fileContent) {
    super($fileNav, $fileContent)
  }

  createContent(_, i) {
    let fileInfo = this.filesInfo[i]
    let $pre = super.createContent(fileInfo.content, i, fileInfo.isError)

    if (fileInfo.content !== fileInfo.raw) {
      let $download = document.createElement('a')
      $download.classList.add('download')

      let file = new Blob([fileInfo.raw], { type: "text/html" })
      let url = URL.createObjectURL(file)
      $download.href = url
      $download.setAttribute('download', fileInfo.name)
      $download.innerHTML = 'Descargar'

      $pre.append($download)
    }
  }
}