Page({
  data: {

  },
  onLoad: function (options) {

  },
  onAuthItemTap: function(e) {
    const type = e.currentTarget.dataset.type;
    console.log('Selected auth type:', type);
    wx.showToast({
      title: '点击了 ' + (type === 'employee' ? '员工认证' : '客户认证'),
      icon: 'none'
    });
  }
});