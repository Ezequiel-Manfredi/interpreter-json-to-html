class FileView {
  constructor($fileNav, $fileContent) {
    this.$fileNav = $fileNav
    this.$fileContent = $fileContent
    this.filesInfo = []
    this.tabActive = this.tabActive.bind(this)
  }

  createTab(name, i) {
    let $tab = document.createElement("button")
    $tab.classList.add("tab")
    if (i === 0) $tab.classList.add("active")
    $tab.setAttribute("content", `t${i}`)
    $tab.addEventListener("click", this.tabActive)
    $tab.innerHTML = name

    this.$fileNav.append($tab)
  }

  createContent(content, i) {
    let $pre = document.createElement("pre")
    if (i !== 0) $pre.classList.add("hidden")
    $pre.id = `t${i}`
    let $content = document.createElement("code")
    $content.innerHTML = content

    $pre.append($content)
    this.$fileContent.append($pre)
    return $pre
  }

  renderFile(file, i) {
    this.filesInfo.push(file)
    this.createTab(file.name, i)
    this.createContent(file.content, i)
  }

  tabActive(e) {
    let $currentTab = e.target
    let currentContentId = $currentTab.getAttribute("content")
    let $currentContent = this.$fileContent.querySelector(`#${currentContentId}`)
    let $activeTab = this.$fileNav.querySelector(".tab.active")
    let contentId = $activeTab.getAttribute("content")
    let $activeContent = this.$fileContent.querySelector(`#${contentId}`)

    $activeTab.classList.remove("active")
    $activeContent.classList.add("hidden")
    $currentTab.classList.add("active")
    $currentContent.classList.remove("hidden")
  }
}