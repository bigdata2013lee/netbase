(function($){
	//前台用户中心的技术服务页面主JS文件。【2014.12.24  jenny】	
	
    /**
	 * 改变工单状态
	 * @method changeStatus
	 * @param {obj} aBtn 事件触发的对象
	 * @param {int} opType 事件触发对象的值
	 * @return {string} 返回一个提示信息并刷新页面
	 */
    var changeStatus = function(aBtn,opType){
        var params={serviceNote:{}}
        params.serviceNote.sid=aBtn.attr("data-id");
        params.serviceNote.status=opType;
        nb.rpc.serviceNoteViews.c("changeTicketStatus",params)
        .success(function(msg){
        	nb.AlertTip.storeCookie(msg);
        	window.location.reload();
        })     
    } 
       
    /**
	 * 改变类表拍讯图标
	 * @method changeSortType
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
	 * 获取类表标题属性值
	 * @method getSortType
	 */
    var getSortType = function(sortType){
        if(sortType == "-1"){sortType = "1";}else{sortType = "-1";};
        return sortType;
    }
    
    $(document).ready(function(){
        changeSortType();   
     
     	//绑定并触发关闭工单事件
		$(".data_table a[action=close]").bind("click", function(){
			changeStatus($(this),1);
		})
		
       	//绑定并触发打开工单事件
		$(".data_table a[action=reopen]").bind("click", function(){
			changeStatus($(this),0);
		})
		
       	//绑定并触发查询工单事件
		$(".query_tool_bar select[name=status]").bind("change",function(){
			var status = $(this).val();
			window.location.href = "/settings/services/?status="+ status;
		});
		
       	//绑定并触发工单评价窗体显示事件
		$(".data_table a[action=audit]").bind("click", function(){
			var ticketId = $(this).attr("data-id");
			nb.uiTools.showEditDialogWin(null, "#appraisement_win", {title:"服务评价",width:700, height:530});
			$("#ticketId").val(ticketId);
		})
		
       	//绑定并触发删除工单事件
		$(".data_table a[action=delete]").bind("click", function(){
			var snId = $(this).attr("data-id");
			nb.uiTools.confirm("你确定要删除吗？",function(){
	          	var params={}
		        params.snId=snId;
		        nb.rpc.serviceNoteViews.c("delServiceNote",params)
		        .success(function(msg){
					nb.AlertTip.storeCookie(msg);
		            window.location.reload();
		        })           
			})
		})
		
       	//绑定并触发工单排序事件
		$(".data_table thead tr th").bind("click",function(){
			var sortFiled = $(this).attr("name");          
			var sType = $(this).children("em").attr("sortType");  
			sortType = getSortType(sType);
			var status = $(".query_tool_bar select[name=status]").find("option:selected").val();
			window.location.href = "/settings/services/?pageNum=1&status="+ status+"&sortFiled="+sortFiled+"&sortType="+sortType;
		})
		
       	//绑定并触发进入工单对话事件
		$(".data_table tbody tr td.hrefcss").bind("click",function(){
      		window.location.href = "/settings/servicesNoteDetail/?dataId="+$(this).parent("tr.data_tr").attr("data-Id");
		})

		// nb.uiTools.setAreaSelect();
		//定义工单对话编辑器
		$("#appraisement_win textarea[name=content]").kendoEditor({});
    });
})(jQuery);
