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
    $inputElement.innerHTML = `>>> ${input}<br/><br/>`
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
    const { tokens, no_tokens, numbers, dates, strings, is_empty } = results
    let outputString = ''

    if (is_empty) {
      return [stringToScan, '<li>Error: imput vacio</li><br/>']
    }
    if (no_tokens.length > 0) {
      outputString += `<li>${this.renderToken(no_tokens, true)}</li><br/>`
    }
    if (numbers.length > 0) {
      outputString += `<li>${this.renderErrors('Numbers', 'los siguientes numeros', numbers)}</li><br/>`
    }
    if (dates.length > 0) {
      outputString += `<li>${this.renderErrors('Dates', 'las siguientes fechas', dates)}</li><br/>`
    }
    if (strings.length > 0) {
      outputString += `<li>${this.renderErrors('Strings', 'los siguientes strings', strings)}</li><br/>`
    }
    if (tokens.length > 0) {
      outputString += `<li>${this.renderToken(tokens)}</li><br/>`
    }

    return [stringToScan, outputString]
  }

  renderErrors(type, msj, data) {
    let description = `<p>Lexer Error (${type}): ${msj} no cumplen las condiciones</p>`
    let elements = data.reduce((acc, element) => {
      let subDescription = `<p>◢ ${element.value}</p>`
      let errors = element.errors.reduce((acc, error) => acc + `<li>► error: ${error}</li>`, '')
      return acc + `<li>${subDescription}<ul>${errors}</ul></li>`
    }, '')

    return `${description}<ul>${elements}</ul>`
  }

  renderToken(data, isNot) {
    let description
    if (isNot) {
      description = `<p>Lexer Error (No_Tokens): los siguientes caracteres no se reconocen</p>`
    } else {
      description = `<p>Lexer (Tokens): los siguientes tokens fueron encontrados</p>`
    }
    let elements = data.reduce((acc, element) => {
      // return acc + `▸ ${element.value} ➜  ${isNot ? 'error: caracter ilegal' : `tipo: ${element.type}`}<br/>`
      return acc +
        `<tr>
          <th>${element.value}</th>
          <th>${element.type}</th>
        </tr>`
    }, '')

    return `${description}
    <table>
      <thead>
        <tr>
          <th>Lexema</th>
          <th>Tipo</th>
        </tr>
      </thead>
      <tbody>
        ${elements}
      </body>
    </table>`
  }

  /*
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
    inputString += `<span ${isNoToken ? 'class="error"' : ''}>
      ${currentString.slice(0, currentString.length)}
    </span>`

    return [inputString, outputString]
  }
  */

  renderNewHistory(stringToScan) {
    this.createNewHistoryItem(stringToScan)
  }
}