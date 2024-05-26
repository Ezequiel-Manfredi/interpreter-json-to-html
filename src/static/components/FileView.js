class FileView {
  constructor($fileNav, $fileContent) {
    this.$fileNav = $fileNav
    this.$fileContent = $fileContent
    this.tabActive = this.tabActive.bind(this)
  }

  createTab(name, i) {
    let tab = document.createElement("button")
    tab.classList.add("tab")
    if (i === 0) tab.classList.add("active")
    tab.setAttribute("content", `t${i}`)
    tab.addEventListener("click", this.tabActive)
    tab.innerHTML = name

    let close = document.createElement("button")
    close.classList.add("close")
    close.innerHTML = "✖️"
    close.addEventListener("click", this.deleteFile)

    tab.append(close)
    this.$fileNav.append(tab)
  }

  createContent(msj, i) {
    let pre = document.createElement("pre")
    if (i !== 0) pre.classList.add("hidden")
    pre.id = `t${i}`
    let content = document.createElement("code")
    content.classList.add("content")
    content.innerHTML = msj

    pre.append(content)
    this.$fileContent.append(pre)
  }

  renderFile(file, i) {
    this.createTab(file.name, i)
    this.createContent(file.msj, i)
  }

  tabActive(e) {
    let currentTab = e.target
    let currentContentId = currentTab.getAttribute("content")
    let currentContent = this.$fileContent.querySelector(`#${currentContentId}`)
    let activeTab = this.$fileNav.querySelector(".tab.active")
    let contentId = activeTab.getAttribute("content")
    let activeContent = this.$fileContent.querySelector(`#${contentId}`)

    activeTab.classList.remove("active")
    activeContent.classList.add("hidden")
    currentTab.classList.add("active")
    currentContent.classList.remove("hidden")
  }

  deleteFile(e) {
    e.stopPropagation()
    console.log("archivo eliminado")
  }
}