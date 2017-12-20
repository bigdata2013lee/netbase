(function($){
	//前台用户中心的 运维商页面的主JS文件【2014.12.19  jenny】
    var m = new nb.xutils.Observer();
    //定义一个技术领域下拉列表控件
    var autoComplateWidget1 = nb.BaseWidgets.extend("autoComplateWidget",{},{_panel_id:"#autoComplateWidget1"});
    
    /**
	 * 根据条件查询运维商
	 * @method searchOperationers
	 */
	var searchOperationers=function(){
		var technologyFileds = autoComplateWidget1.getSelectedItems().join(",");
		var href="/ucenter/operationerList/?technologyFileds=" + encodeURIComponent(technologyFileds);
		location.href = href;
	};
   
   
    $(document).ready(function(){        
	    //初始化一个技术领域下拉列表控件  
        autoComplateWidget1.__init__();
        
        //触发查询运维商事件
        $("#search_box button").bind("click", function(){
            searchOperationers();
        });     
    });
    
})(jQuery);
