(function($){
	//工程师用户后台我的客户页面主JS文件 【2014.12.24  jenny】	
    var m = window.customers = {};
    
    //定义一个显示工程师的服务客户列表的组件
    m.customersWidget = nb.BaseWidgets.extend("BaseListWidget",{
        _panel_id: "#customersWidget",
        remoteView:nb.rpc.engineerViews,
        remoteMethod:"getCustomers",
        getRemoteParams:function(){ return {uid: userName}; }
    })
    
	//定义一个显示工程师的服务客户的最新事件窗体组件
    m.showNewEventWidget = nb.BaseWidgets.extend("BaseListWidget", {
        _panel_id:"#showNewEventWin",
        remoteMethod:"getCustomerIssues",
        remoteView:nb.rpc.engineerViews,
        customerUid:null,
        getRemoteParams: function(){return {customerUid: this.customerUid}},

        afterInit: function(){
            var self = this;
            $("#customersWidget").delegate("button[name=btNewEvent]", "click", function(){
            	self.customerUid = $(this).attr("customerUid");
                nb.uiTools.showEditDialogWin(null, self._panel_id, {width:800, height:400, title: "最新事件列表"});
                self.reload();
             });
        }
    });	
	    
    $(document).ready(function(){
    	//初始化并加载一个显示工程师的服务客户列表的组件
        m.customersWidget.reload();
		//初始化一个显示工程师的服务客户的最新事件窗体组件
        m.showNewEventWidget.__init__();
    });
    
    
})(jQuery);
