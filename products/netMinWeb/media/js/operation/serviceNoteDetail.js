(function($){
	//运维商用户中心的工程师管理的工单检索和评价报表界面的主JS【2014.12.19  jenny】
	
    /**
	 * 改变页面列表的排序图标
	 * @method changeSortType
	 * 1、获取列表table的标题行的字段
	 * 2、获取标题行字段的对应的图标元素
	 * 3、根据标题字段的属性sortType的值来移除添加对应的样式
	 */
    var changeSortType = function(){
        var thread ;
        if($("table.data_table thead tr th span").length > 0){
            thread = $("table.data_table thead tr th span");
        }else{
            thread = $("table.data_table thead tr th");
        }
        var emList = thread.children("em");
        for(i = 0; i< emList.length;i++){
            var sortType = emList.eq(i).attr("sortType");
            if(sortType == "1"){
                emList.eq(i).removeClass("downImg").addClass("upImg");
            }else{
                emList.eq(i).removeClass("upImg").addClass("downImg");
            }
        }
    }
    
    /**
	 * 根据当前标题字段元素的属性sortType获取相反的值
	 * @method getSortType
	 * @param {string} sortType 当前标题字段元素的属性sortType的值
	 * @return 返回与当前标题字段元素的属性sortType相反的值
	 */
    var getSortType = function(sortType){
        if(sortType == "-1"){sortType = "1";}else{sortType = "-1";};
        return sortType;
    }
    
    $(document).ready(function(){
		//触发工单检索页面列表排序的事件
		$("table[name=listServiceNotes] thead th").bind("click",function(){
			var sortFiled = $(this).attr("name");          
			var sType = $(this).children("em").attr("sortType");         
			sortType = getSortType(sType);
			var status = $(".query_tool_bar select[name=status]").find("option:selected").val();
			window.location.href = "/operation/listServiceNotes/?pageNum=1&status="+ status+"&sortFiled="+sortFiled+"&sortType="+sortType;
		})
		
		//触发评价报表页面列表排序的事件
		$("table[name=listAppraisements] thead th").bind("click",function(){
			var sortFiled = $(this).attr("name");          
			var sType = $(this).children("em").attr("sortType");         
			sortType = getSortType(sType);
			window.location.href = "/operation/listAppraisements/?pageNum=1&sortFiled="+sortFiled+"&sortType="+sortType;
		})
      
      	//触发进入评价详情页面
		$("table[name=listAppraisements] tbody tr").bind("click",function(){
			engId = $(this).attr("engId");
			window.location.href = "/operation/listEngAppraisements/?engId="+engId;
		})
		
		//触发评价详情页面的列表排序事件
		$("table[name=listEngAppraisements] thead th").bind("click",function(){
			var engId = $("table[name=listEngAppraisements]").attr("data-id");
			var sType = $(this).children("em").attr("sortType");         
			sortType = getSortType(sType);
			var sortFiled = $(this).attr("name");          
			window.location.href = "/operation/listEngAppraisements/?pageNum=1&sortFiled="+sortFiled+"&engId="+engId+"&sortType="+sortType;
		})
		
		//触发工单检索页面查询事件
		$(".query_tool_bar select[name=status]").bind("change",function(){
			var status = $(this).val();
			window.location.href = "/operation/listServiceNotes/?status="+ status;
		});
		  
		changeSortType();
        
    });
    
})(jQuery);
