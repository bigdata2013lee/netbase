(function($) {
	//前台用户中心的事件页面，生成工单的主JS文件 【2014.12.19  jenny】	
	
    var m = window.eventsIndex = {};
    var grid = null;
    //定义一个
    var ticketAutoComplateWidget = nb.BaseWidgets.extend("autoComplateWidget", {},{_panel_id:"#ticketAutoComplateWidget"});
    
    /**
	 * 获取服务器时间
	 * @method getServerTime
	 * @return {string} 返回一个时间戳
	 */
    var getServerTime = function(){
		var xmlHttp = false; 
		//获取服务器时间 
		try { 
			xmlHttp = new ActiveXObject("Msxml2.XMLHTTP"); 
		} catch (e) { 
			try { 
				xmlHttp = new ActiveXObject("Microsoft.XMLHTTP"); 
			} catch (e2) { 
				xmlHttp = false; 
			} 
		} 
		  
		if (!xmlHttp && typeof XMLHttpRequest != 'undefined') { 
			xmlHttp = new XMLHttpRequest(); 
		} 
		     
		xmlHttp.open("GET", "", false); 
		xmlHttp.setRequestHeader("Range", "bytes=-1"); 
		xmlHttp.send(); 
		  
		var severtime=new Date(xmlHttp.getResponseHeader("Date")); 
		return severtime;
	}
    
    /**
	 * 验证提交工单的数据
	 * @method _validateParams
	 * @param {string} subject 工单主题
	 * @param {string} dueTime 工单期限
	 * @param {string} emergencyDegree 工单紧急度
	 * @param {string} content 工单内容
	 * @return {bool} 返回一个bool值，如果不成功，还会显示一个提示信息
	 */
    var _validateParams = function(params){
        var em = $("#createTicket_win div.validateErrorMsg");
        var rules = {
            subject:function(val){return val.replace(/\s/ig,'').split("<p></p>").join("").length<=20 && val.replace(/\s/ig,'').split("<p></p>").join("").length >0},
            dueTime:function(val){
            	if(!val){
            		return false
        		}else{
        			var val1 = new Date(val);
        			return val1.getTime() >= params.serverTime.getTime()
    			}
        	},
            emergencyDegree:"required",
            content:function(val){return val.replace(/\s/ig,'').split("<p></p>").join("").length<=1000 && val.replace(/\s/ig,'').split("<p></p>").join("").length >0}
        };
        var messages = {
            subject:"请输入20字以内的标题",
            dueTime:"时间期限必须比当前时间晚",
            emergencyDegree:"请选择话题所属的领域",
            content:"请输入1000字以内的内容"
        };
        var validator = new nb.xutils.Validator(em, rules, messages);
        return validator.validate(params);            
    };
    
    /**
	 * 提交工单数据
	 * @method _validateParams
	 * @param {string} event 事件ID
	 * @return {string} 如果数据通过验证提交到后台了，则返回一个是否成功的提示信息，并关闭窗体，刷新页面
	 */
    var createServiceNote = function(event){
        var eventInfo = event.toJSON();
        var serviceNote = {};
        serviceNote.eventSeverity = eventInfo.severity;
        serviceNote.title = eventInfo.message;
        serviceNote.summary = eventInfo.message;
        serviceNote.monitorObjName = eventInfo.title;
        serviceNote.eventId = eventInfo._id;
        serviceNote.eventLabel = eventInfo.label;
        serviceNote.status=0;
        serviceNote.subject = $("#createTicket_win input[name=subject]").val();
        serviceNote.emergencyDegree = $("#createTicket_win select[name=emergencyDegree]").val();
        serviceNote.content = $("#createTicket_win textarea[name=content]").data("kendoEditor").value();
        var dueTime = $("#createTicket_win input[name=dueTime]").data("kendoDatePicker").value();

		var serverTime = getServerTime();
		var totalDate ="";
		if(dueTime){
			totalDate = dueTime.toLocaleDateString() +" " +serverTime.getHours()+":"+serverTime.getMinutes()+":"+serverTime.getSeconds()			
		}
		serviceNote.dueTime = new Date(totalDate);
		serviceNote.serverTime = serverTime;

		if(!_validateParams(serviceNote))return;
		delete serviceNote.nt;
        nb.rpc.serviceNoteViews.c("createServiceNote", {serviceNote: serviceNote}).
        success(function(msg){
            grid.dataSource.read();
           	nb.AlertTip.auto(msg);
            nb.uiTools.closeEditDialogWin("#createTicket_win");
        });
    }
    
    $(document).ready(function() {
        //初始化一个查询控件
        grid = eventsConsole.createGrid("searchEvents");
        //初始化一个编辑器控件
        $("#createTicket_win textarea[name=content]").kendoEditor({});
        //初始化一个日期控件
        $("#createTicket_win .fields input.dueTime").kendoDatePicker();
       	var dataUid="";
        //触发创建工单的窗体显示事件
        $("#data-grid").delegate("a[name=createServiceNote]", "click", function(evt){
            nb.uiTools.showEditDialogWin(null, "#createTicket_win", {title:"服务单",width:650, height:440});
            dataUid = $(this).closest("tr").attr("data-uid");
        });
        //触发提交工单数据的事件
        $("#createTicket_win .win_opbar button.ok").bind("click",function(){
            var evt = grid.dataSource.getByUid(dataUid);
            createServiceNote(evt);
        });

    });

})(jQuery);
