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
          let nameHtml = file.name.replace('json', 'html')
          if (output.ok) {
            let stringTreatment = output.content
              .replace(/\</g, '&lt;').replace(/\>/g, '&gt;')

            return {
              name: nameHtml,
              content: stringTreatment,
              raw: output.content
            }
          } else {
            return {
              name: nameHtml,
              content: output.errors,
              raw: output.errors
            }
          }
        })
      )
    }

    return outputFiles
  }
}