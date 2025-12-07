Page({
  data: {
    navBarHeight: 0,
    statusBarHeight: 0,
    menuButtonHeight: 0,
    menuButtonTop: 0
  },
  onLoad: function (options) {
    // 获取系统信息
    const systemInfo = wx.getSystemInfoSync();
    // 获取胶囊按钮位置信息
    const menuButtonInfo = wx.getMenuButtonBoundingClientRect();
    
    // 状态栏高度
    const statusBarHeight = systemInfo.statusBarHeight;
    // 胶囊按钮高度
    const menuButtonHeight = menuButtonInfo.height;
    // 胶囊按钮上边距 (用于计算导航栏垂直居中)
    const menuButtonTop = menuButtonInfo.top;
    
    // 导航栏整体高度 = 胶囊按钮底部位置 + 胶囊按钮下边距 (通常取胶囊上边距-状态栏高度)
    // 或者简单计算：(胶囊按钮上边距 - 状态栏高度) * 2 + 胶囊按钮高度 + 状态栏高度
    // 这里我们直接计算导航栏内容区域（不含状态栏）的高度和内边距
    
    // 导航内容区高度（不含状态栏）
    const navContentHeight = (menuButtonTop - statusBarHeight) * 2 + menuButtonHeight;
    
    // 总导航栏高度
    const navBarHeight = statusBarHeight + navContentHeight;

    this.setData({
      statusBarHeight,
      navBarHeight,
      menuButtonHeight,
      menuButtonTop,
      navContentHeight
    });
  }
})
