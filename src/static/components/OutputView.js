class OutputView extends FileView {
  constructor($fileNav, $fileContent) {
    super($fileNav, $fileContent)
  }

  createContent(_, i) {
    let fileInfo = this.filesInfo[i]
    console.log(fileInfo)
    let $pre = super.createContent(fileInfo.content, i)

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