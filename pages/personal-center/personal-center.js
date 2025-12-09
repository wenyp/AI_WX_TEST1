Page({
  data: {
    navBarHeight: 0,
    statusBarHeight: 0,
    menuButtonHeight: 0,
    menuButtonTop: 0,
    navContentHeight: 0
  },
  onLoad() {
    const systemInfo = wx.getSystemInfoSync()
    const menuButtonInfo = wx.getMenuButtonBoundingClientRect()
    const statusBarHeight = systemInfo.statusBarHeight
    const menuButtonHeight = menuButtonInfo.height
    const menuButtonTop = menuButtonInfo.top
    const navContentHeight = (menuButtonTop - statusBarHeight) * 2 + menuButtonHeight
    const navBarHeight = statusBarHeight + navContentHeight
    this.setData({
      statusBarHeight,
      navBarHeight,
      menuButtonHeight,
      menuButtonTop,
      navContentHeight
    })
  },
  goHome() {
    const pages = getCurrentPages()
    if (pages && pages.length > 1) {
      wx.navigateBack()
    } else {
      wx.navigateTo({ url: '/pages/demo/demo' })
    }
  },
  handleBack() {
    const pages = getCurrentPages()
    if (pages.length > 1) {
      wx.navigateBack()
    } else {
      wx.navigateTo({ url: '/pages/index/index' })
    }
  },
  handleSettingsClick() {
    wx.navigateTo({
      url: '/pages/settings/settings'
    })
  },
  handleIdentityAuthClick() {
    wx.navigateTo({
      url: '/pages/identity-auth/identity-auth'
    })
  }
})
