(function($){
    
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
    
    var editServiceMark = function(){                
        var params = {};
        var attitude = $(".service_attitude span").attr("index");
        var techLevel =  $(".professional_level span").attr("index");
        var responseSpeed =  $(".response_speed span").attr("index");
        var ticketId = $("#ticketId").val();
        var appraiseContent = $("#appraisement_win textarea[name=content]").data("kendoEditor").value();
        params.attitude = attitude;
        params.techLevel = techLevel;
        params.responseSpeed = responseSpeed;
        params.appraiseContent = appraiseContent;
        params.ticketId = ticketId;
        
        if(!validateEditServiceMark(params)){return};
        nb.rpc.serviceNoteViews.c("appraise",params)
        .success(function(msg){
            nb.AlertTip.auto(msg);        
            nb.uiTools.closeEditDialogWin("#appraisement_win");
        });
        
        
    }
    
    $(document).ready(function(){       
         
        $("dl.fields").delegate('li[mark=start]','click',function(){
            degree =['','很差','差','中','良','优']
            var num = $(this).attr("index");
            $(this).removeClass("level_hollow").addClass("li_hover");
            $(this).prevAll("li").removeClass("level_hollow").addClass("li_hover");
            $(this).nextAll("li").removeClass("li_hover").addClass("level_hollow");

            $(this).siblings("span.leve_tip").html(degree[num]);
            $(this).siblings("span.leve_tip").attr("index",num);
        })
        
        $("#appraisement_win .win_opbar button.ok").bind("click",function(){
            editServiceMark();
        });

    });
    
    
})(jQuery);
