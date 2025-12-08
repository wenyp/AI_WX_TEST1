Page({
  data: {
    menuItems: [
      { id: 1, title: '个人信息', url: '' },
      { id: 2, title: '我的地址', url: '' },
      { id: 3, title: '用户协议', url: '' },
      { id: 4, title: '隐私管理', url: '' },
      { id: 5, title: '退出登录', url: '' }
    ]
  },

  onLoad(options) {

  },

  handleItemClick(e) {
    const item = e.currentTarget.dataset.item;
    console.log('Clicked:', item.title);
    // TODO: Handle navigation based on item.url or id
  }
})