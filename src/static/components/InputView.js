class InputView extends FileView {
  constructor($fileNav, $fileContent) {
    super($fileNav, $fileContent)
  }

  async fetchFilesParse() {
    let outputFiles = []
    for (const file of this.filesInfo) {
      outputFiles.push(await fetch('/parser', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: file.content })
      }).then(res => res.json())
        .then(output => {
          let name = file.name.replace('json', 'html')
          let content = ''
          let raw = ''
          if (output.ok) {
            content = output.content
              .replace(/\</g, '&lt;').replace(/\>/g, '&gt;')
            raw = output.content
          } else {
            content = output.errors.reduce((acc, err) => {
              return `${acc}<p>${err.msj} (${err.line},${err.pos})</p>`
            }, '')
            raw = content
          }
          return {
            name,
            content,
            raw
          }
        })
      )
    }

    return outputFiles
  }
}