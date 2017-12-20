(function($){
    var m = window.nginx_list = new nb.xutils.Observer();

    
    
    
    $(document).ready(function() {
        
        
        $("#data_table_1").delegate("a[action=detail]","click", function(){
        	nb.uiTools.showEditDialogWin(null, "#detail_win",{title:"nginx祥细", width:800, height:500});
        	$("#detail_win iframe").attr("src", "/middleware/nginx_view/" + $(this).attr("mwuid") + "/");
        });
        
        $("#data_table_1").delegate("a[action=delMw]","click", function(){
        	if(!window.confirm("你确定删除此服务器?")){return;}
        	nb.rpc.middlewareViews.c("removeNginx",{uid: $(this).attr("mwuid")})
        	.success(function(msg){
        		nb.AlertTip.storeCookie(msg);
        		window.location.href="/middleware/nginx_list/";
        	})
        });
        
    });
 
})(jQuery);
