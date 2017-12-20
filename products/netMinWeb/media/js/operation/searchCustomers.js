(function($){
	//运维商用户中心的客户中心，检索客户页面的主JS文件【2014.12.19  jenny】
    var m = new nb.xutils.Observer();
    
    /**
	 * 提交要收藏的客户
	 * @method favoriteCustomer
	 * @param {string} customerId 收藏用户的ID
	 * @return {string} 通过Ajax的方式将参数传至后台，成功与否返回一个提示信息的字符串
	 */
    var favoriteCustomer = function(customerId){
        var params = {customerId:customerId};
        nb.rpc.operationView.c("addFavoriteCustomer", params)
        .success(function(msg){
            nb.AlertTip.auto(msg);
        });
    };

    /**
	 * 提交要添加的客户
	 * @method addCustomer
	 * @param {string} username 收藏用户的账号
	 * @return {string} 通过Ajax的方式将参数传至后台，成功与否返回一个提示信息的字符串
	 */
    var addCustomer = function(username){
        var params={};
        params.customerUsername = username
        nb.rpc.operationView.c("addServiceCustomer", params)
        .success(function(msg){
            nb.AlertTip.auto(msg);
        });
    }
    
    /**
	 * 查询客户
	 * @method searchCustomers
	 * @return {obj} 提交一个包含页码和邮箱字段参数的查询到后台，返回一个对象到前台页面加载渲染
	 */
    var searchCustomers = function(){
        var email = $("div.custtomers_search_box input[name=email]").val();
        location.href="/operation/searchCustomers/?pageNum=1&email=" + encodeURIComponent(email);
    }
    
    $(document).ready(function(){
        //触发添加客户的事件
        $("a[action=add]").bind("click",function(){
             var username=$(this).attr("username");
             addCustomer(username);          
        });
        
        //触发收藏客户的事件
        $("a[action=favorite]").bind("click",function(){
             var customerId=$(this).attr("customerId");
             favoriteCustomer(customerId);          
        });
        
        //触发查询客户的事件
        $("#search_btn").bind("click",function(){
            searchCustomers();
        });
    });
})(jQuery);     