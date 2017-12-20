(function($){
		
	//原本为运维商用户中心的客户中心的收藏客户页面的JS，现在该js和html文件没有使用，暂时该js文件为预留文件，后期可删除【2014.12.18  jenny】
	
    var m = new nb.xutils.Observer();
    
    var remarkFavoriteCustomer=function(){
        var params=nb.uiTools.mapFields("#editServiceCustomerWin");
        nb.rpc.operationView.c("remarkFavoriteCustomer", params)
        .success(function(msg){
            nb.AlertTip.storeCookie(msg);
            nb.uiTools.closeEditDialogWin("#editServiceCustomerWin");
            location.reload();
        });
    };

    var removeFavoriteCustomer = function(favoriteCustomerId){
        var params={favoriteCustomerId:favoriteCustomerId};
        nb.rpc.operationView.c("removeFavoriteCustomer", params)
        .success(function(msg){
            nb.AlertTip.storeCookie(msg);
            location.href="/operation/favoriteCustomers/?pageNum=1";
        });
    }
    
    var searchFavoriteCustomers = function(){
        var companyName = $("div.fav_custtomers_search_box input[name=companyName]").val();
        location.href="/operation/favoriteCustomers/?pageNum=1&companyName=" + encodeURIComponent(companyName);
    }
    
    $(document).ready(function(){
        
        $("ul.favoriteCustomers_ul .favoriteCustomers_opbar a[action=edit]").bind("click", function(){
            nb.uiTools.showEditDialogWin(null, "#editServiceCustomerWin", {width:500, height:200});
            
            var remark = $(this).closest("li").find("dd[name=remark]").text();
            var favoriteCustomerId = $(this).closest("li").attr("favorite_customer_id");
            
            $("#editServiceCustomerWin input[name=favoriteCustomerId]").val(favoriteCustomerId);
            $("#editServiceCustomerWin dl.fields textarea[name=remark]").text(remark);
        });
        
        $("#editServiceCustomerWin .win_opbar button.ok").bind("click",function(){
            remarkFavoriteCustomer();
        });
        
       
        $("ul.favoriteCustomers_ul .favoriteCustomers_opbar a[action=remove]").bind("click", function(){
            if(!window.confirm("你确定要删除该用户吗？")) return;
            var favoriteCustomerId = $(this).closest("li").attr("favorite_customer_id");
            removeFavoriteCustomer(favoriteCustomerId);
            
        });
        
        $(".fav_custtomers_search_box .fields .searh_btn").bind("click",function(){
            searchFavoriteCustomers();
        })
      
    });
})(jQuery);
