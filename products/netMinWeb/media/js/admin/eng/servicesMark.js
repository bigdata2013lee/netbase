(function($){
	//前台用户评价工单的js文件【2014.12.19  jenny】	

    /**
	 * 验证工单评价数据
	 * @method validateEditServiceMark
	 * @param {string} attitude 服务态度
	 * @param {string} techLevel 专业水平
	 * @param {string} responseSpeed 响应速度
	 * @return {bool} 判断评价数据是否符合要求，如果不符合要求显示提示信息并返回false
	 */
    var validateEditServiceMark = function(params){
        var em = $("#appraisement_win div.validateErrorMsg");
        var rules = {
            attitude:function(val){return val*1 >  0},
            techLevel:function(val){return val*1 >  0},
            responseSpeed:function(val){return val*1 >  0},
        };
        var messages = {
            attitude:"服务态度请给个评分吧",
            techLevel:"专业水平请给个评分吧",
            responseSpeed:"响应速度请给个评分吧"
        };
        var validator = new nb.xutils.Validator(em, rules, messages);
        return validator.validate(params);            
    }
    
    /**
	 * 提交工单评价数据
	 * @method editServiceMark
	 * @return {string} 数据如果通过验证，则通过Ajax提交，返回是否提交成功的提示信息，并关闭窗体
	 */
    var editServiceMark = function(){                
        var params = {};
        var attitude = $(".service_attitude span").attr("index");
        var techLevel =  $(".professional_level span").attr("index");
        var responseSpeed =  $(".response_speed span").attr("index");
        var ticketId = $("#appraisement_win input[type=hidden]").val();
        
        var appraiseContent = $("#appraisement_win textarea[name=content]").data("kendoEditor").value();
        params.attitude = attitude;
        params.techLevel = techLevel;
        params.responseSpeed = responseSpeed;
        params.appraiseContent = appraiseContent;
        params.ticketId = ticketId;
        
        markCount = parseInt(attitude)+parseInt(techLevel)+parseInt(responseSpeed);
        if(markCount<=5){params.appr ="bad"}
        else if (markCount<=10){params.appr ="common"}
        else if (markCount<=15){params.appr ="good"}
        else{params.appr="common"}
        if(!validateEditServiceMark(params)){return};
        nb.rpc.serviceNoteViews.c("appraise",params)
        .success(function(msg){
            nb.AlertTip.auto(msg);        
            nb.uiTools.closeEditDialogWin("#appraisement_win");
        });
    }
    
    $(document).ready(function(){       
        //触发点击评价图表则改变图标颜色的事件
        //颜色改变的同时，将对应的值赋给对应的隐藏控件
        $("dl.fields").delegate('li[mark=start]','click',function(){
            degree =['','很差','差','中','良','优']
            var num = $(this).attr("index");
            $(this).removeClass("level_hollow").addClass("li_hover");
            $(this).prevAll("li").removeClass("level_hollow").addClass("li_hover");
            $(this).nextAll("li").removeClass("li_hover").addClass("level_hollow");

            $(this).siblings("span.leve_tip").html(degree[num]);
            $(this).siblings("span.leve_tip").attr("index",num);
        })
        
        //触发提交添加运维商数据的事件
        $("#appraisement_win .win_opbar button.ok").bind("click",function(){
            editServiceMark();
        });

    });
    
    
})(jQuery);
