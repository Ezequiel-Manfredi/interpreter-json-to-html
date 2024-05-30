class HistoryView {
  constructor($history) {
    this.$history = $history
  }

  async createNewHistoryItem(stringToScan) {
    let $newHistoryItem = document.createElement("li")
    $newHistoryItem.classList.add("item")
    let $inputElement = document.createElement("p")
    let $outputElement = document.createElement("ul")

    let results = await this.fetchResult(stringToScan)
    let [input, output] = this.preprareStrings(stringToScan, results)
    $inputElement.innerHTML = `>>>> ${input}<br/><br/>`
    $outputElement.innerHTML = output


    $newHistoryItem.append($inputElement)
    $newHistoryItem.append($outputElement)
    this.$history.append($newHistoryItem)
    this.$history.scrollTop = this.$history.scrollHeight - $newHistoryItem.scrollHeight
  }

  async fetchResult(stringToScan) {
    return await fetch('/lexer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ string: stringToScan })
    })
      .then(res => res.json())
  }

  preprareStrings(stringToScan, results) {
    let isNoToken = false
    let inputString = ''
    let outputString = ''
    let currentString = stringToScan
    let prevPos = 0
    let endPos = 0
    results.forEach(token => {
      console.log(inputString, " ", currentString)
      if (token.type === 'NO_TOKEN') {
        isNoToken = true
        endPos = token.lexpos - prevPos
        prevPos = token.lexpos
        inputString += `<span>${currentString.slice(0, endPos)}</span>`
        currentString = currentString.slice(endPos)
      } else if (isNoToken) {
        isNoToken = false
        let endPos = token.lexpos - prevPos
        inputString += `<span class="error">${currentString.slice(0, endPos)}</span>`
        currentString = currentString.slice(endPos)
        prevPos = token.lexpos
      }
      outputString += `<li>
        ${token.value} ➜ tipo: ${token.type} , linea: ${token.lineno} , posicion: ${token.lexpos}<br/>
      </li>`
    })
    inputString += `<span ${isNoToken ? 'class="error"' : ''}>${currentString.slice(0, currentString.length)}</span>`

    return [inputString, outputString]
  }

  renderNewHistory(stringToScan) {
    this.createNewHistoryItem(stringToScan)
  }
}