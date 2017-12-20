(function($){
	//运维商用户中心的客户中心界面的主JS【2014.12.19  jenny】
    var m = new nb.xutils.Observer();
    
    /**
	 * 提交指派工程师的数
	 * @method appointServiceEngineer
	 * @param {string} operationServiceCustomerId 服务客户的ID
	 * @param {string} engineerId 工程师的ID
	 * @return {string} 通过Ajax方式将参数传到后台，返回成功与否的提示信息
	 */
    var appointServiceEngineer = function(){
        var params = nb.uiTools.mapFields("#appointServiceEngineerWin");
        nb.rpc.operationView.c("appointServiceEngineer", params)
        .success(function(msg){
            nb.AlertTip.storeCookie(msg);
            nb.uiTools.closeEditDialogWin("#appointServiceEngineerWin");
            location.reload();
        });        
    }

    
    $(document).ready(function(){
        
        //触发指派工程师窗体弹出事件，并把当前服务客户的ID付给窗体中的隐藏控件
        $("a[action=appointServiceEngineer]").bind("click", function(){
            var operationServiceCustomerId = $(this).attr("customer_id");
            $("#appointServiceEngineerWin input[name=operationServiceCustomerId]").val(operationServiceCustomerId);
            nb.uiTools.showEditDialogWin(null, "#appointServiceEngineerWin", {width:500, height:200});            
        });
        
        //触发指派工程师提交数据事件
        $("#appointServiceEngineerWin .win_opbar button.ok").bind("click",function(){
            appointServiceEngineer();
        });
        
        //触发删除收藏客户事件，并返回一个成功与否的提示信息
        $("a[action=deleteFavorite]").bind("click",function(){
            var favoriteCustomerId = $(this).attr("favorite_customer_id");
			nb.uiTools.confirm("你确定要删除此收藏客户吗？",function(){
				var params = {}
				params.favoriteCustomerId = favoriteCustomerId;
				nb.rpc.operationView.c("removeFavoriteCustomer", params)
				.success(function(msg){
					nb.AlertTip.storeCookie(msg);
					window.location.reload();
				})           
			})          
        });
        
        //触发删除服务客户的事件，并返回一个成功与否的提示信息
        $("a[action=delelteCustomer]").bind("click",function(){
            var serviceCustomerId = $(this).attr("service_customer_id");
			nb.uiTools.confirm("你确定要删除此服务客户吗？",function(){
				var params={}
				params.serviceCustomerId = serviceCustomerId;
				nb.rpc.operationView.c("removeCustomer", params)
				.success(function(msg){
					nb.AlertTip.storeCookie(msg);
					window.location.reload();
				})           
			})			
        });
    });
})(jQuery);
