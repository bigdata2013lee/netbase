(function($){
	//前台用户和工程师用户的服务记录页面的js文件【2014.12.19  jenny】	
	
    /**
	 * 改变工单状态事件【改事件不做单独触发，在表单提交时一同由有后台处理 2014.12.22】
	 * @method changeStatus
	 * @param {string} aBtn 工单ID
	 * @param {int} opType 改变状态：打开/关闭
	 * @return {string} 把参数通过Ajax的方式传到后台，返回成与否的提示信息，并重新加载页面
	 */
    var changeStatus = function(aBtn,opType){
        var params = {serviceNote:{}}
        params.serviceNote.sid = aBtn;
        params.serviceNote.status = opType;
        nb.rpc.serviceNoteViews.c("changeTicketStatus",params)
        .success(function(msg){
            nb.AlertTip.auto(msg);
            window.location.reload();
        })     
    }    
    
    /**
	 * 改变列表排序
	 * @method changeSortType
	 * 点击列表列头时，改变排序图标的
	 */
    var changeSortType = function(){
        var thread = $("table.data_table thead tr th");
        var emList = thread.children("em");
        for(i = 0; i< emList.length;i++){
            var sortType = emList.eq(i).attr("sortType");
            if(sortType == "1"){
                emList.eq(i).removeClass("downImg").addClass("upImg");
            }
        }
    }
    
    /**
	 * 获取列表标头的sortType属性值
	 * @method getSortType
	 * @return {string} 返回一个排序值
	 */
    var getSortType = function(sortType){
        if(sortType == "-1"){sortType = "1";}else{sortType = "-1";};
        return sortType;
    }

    $(document).ready(function(){
		changeSortType();     
    	
    	// //触发改变工单状态的事件
		// $("#form1 select.common").bind("change", function(){
			// var status = $("input[name=snUid]").val();
			// var selectT = $(this).val();
			// if(selectT == "1"){changeStatus(status,1)};
		// })
    
    	//触发查询不同状态的工单的事件
		$(".query_tool_bar select[name=status]").bind("change",function(){
			var status = $(this).val();
			window.location.href = "/engineer/services/?status="+ status;
		});
		
		//触发店家列表表头改变排序事件
		$(".data_table thead tr th").bind("click",function(){
			var sortFiled = $(this).attr("name");                  
			var sType = $(this).children("em").attr("sortType");  
			sortType = getSortType(sType); 
			var status = $(".query_tool_bar select[name=status]").find("option:selected").val();
			window.location.href = "/engineer/services/?pageNum=1&status="+ status+"&sortFiled="+sortFiled+"&sortType="+sortType;
		})
		
		//触发点击类表数据，进入工单详情页面  
		$(".data_table tbody tr td.hrefcss").bind("click",function(){
			window.location.href = "/engineer/servicesNoteDetail/?dataId="+$(this).parent("tr.data_tr").attr("data-Id");
		})

    });
})(jQuery);
