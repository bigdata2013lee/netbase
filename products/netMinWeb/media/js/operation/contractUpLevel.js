(function($){
	
	//原本为合约升级页面js,现在已经没有合约升级这个功能，而改为设备扩展，暂时改js文件为预留文件，后期可删除【2014.12.18  jenny】
    var m = new nb.xutils.Observer();
	
    var validateUpLevel=function(params){
        var em = $("#upLevelWin div.validateErrorMsg");
        var rules = {
            contarctName:"required",
            originalName:"required" ,
            // contactPhone:"required"  ,
            contactPhone: {method: "regex", exp: /((\d{11})|^((\d{7,8})|(\d{4}|\d{3})-(\d{7,8})|(\d{4}|\d{3})-(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})|(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1}))$)/},         
        };
        var messages = {
            contarctName:"合约名称是必选项，请选择",
            originalName:"姓名是必填项，请输入",
            contactPhone:"联系电话格式有误，请重新输入"
        };
        var validator = new nb.xutils.Validator(em, rules, messages);
        
        return validator.validate(params);            
    };
        
    var upLevel = function(){
        var params=nb.uiTools.mapFields("#upLevelWin");
         if(!validateUpLevel(params)){return;}
        nb.rpc.operationView.c("upLevel", params)
        .success(function(msg){
            nb.AlertTip.auto(msg);
            //location.reload();
        });
        nb.uiTools.closeEditDialogWin("#upLevelWin");
    }
    
    $(document).ready(function(){
          $("div.upTip a[action=upLevel]").bind("click",function(){
            $("div.upTip p").css({"display":"block"});
            setTimeout(function(){$("div.upTip p").css({"display":"none"});}, 1000*5);              
            nb.uiTools.showEditDialogWin(null, "#upLevelWin", {width:680, height:480});  
            $("div#upLevelWin dl.fields input[type=radio]").attr("checked",false);             
        })
        
        $("#upLevelWin .win_opbar button.ok").bind("click",function(){
                upLevel();
        });
        
        $("div#upLevelWin dl.fields input[type=radio]").bind("click",function(){
            var val = $(this).val();
            $("div#upLevelWin ul>li").hide();
            $("div#upLevelWin ul>li." + val).show();
        })
        
    });
    
})(jQuery);
