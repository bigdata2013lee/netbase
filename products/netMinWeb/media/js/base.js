(function($){
     var m = new nb.xutils.Observer();
    var  questionAutoComplateWidget = nb.BaseWidgets.extend("autoComplateWidget", {},{_panel_id:"#questionAutoComplateWidget"});
    var  shareAutoComplateWidget = nb.BaseWidgets.extend("autoComplateWidget", {},{_panel_id:"#shareAutoComplateWidget"});
    console.info(questionAutoComplateWidget);
    
    var checkVariable=function(tmp,info){
        if(tmp=="" || tmp==[] || tmp=={}) {
            nb.AlertTip.auto(info);
            exit();
        }
    }
    
    var checkVarDic=function(varDic){
        checkVariable(varDic.title,"请输入标题")
        checkVariable(varDic.area.d0,"请选择您所在的省份")
        checkVariable(varDic.area.d1,"请选择您所在的城市")
        checkVariable(varDic.fields,"请选择话题所属的领域")
        checkVariable(varDic.content,"请输入内容")
        if (varDic.award){
          if(varDic.award.aType != "不悬赏") checkVariable(varDic.award.value,"请输入悬赏金额");  
          if(varDic.award.aType == "积分") {
              var awardNum=$("#createQuestion_win span[name=awardNum]").text();
              if(awardNum<=0 || awardNum<varDic.award.value) checkVariable("","积分余额不足，您当前的积分为"+awardNum); 
          }  
        } 
    }
    var createQuestion=function(){
        var win = $("#createQuestion_win");
        
        var params={};
        var title=$("#createQuestion_win input[name=title]").val();
        var content = $("#createQuestion_win textarea[name=content]").data("kendoEditor").value();
        var d0=$("#createQuestion_win select[name=province]").val();
        var d1=$("#createQuestion_win select[name=city]").val();
        
        var fields=questionAutoComplateWidget.getSelectedItems().join(",");
        fields=fields.split(",")
        var aType=$("#createQuestion_win select[name=aType]").val();
        var value=$("#createQuestion_win input[name=value]").val();
        params.title=title
        params.content=content
        params.area={"d0":d0,"d1":d1}
        params.fields=fields
        params.award={"aType":aType,"value":value}
        checkVarDic(params)
        
        nb.rpc.topicViews.c("createQuestion",params)
        .success(function(msg){
            nb.AlertTip.auto(msg);
        });
        
        nb.uiTools.closeEditDialogWin("#createQuestion_win");
        
        
    }
    
     var createShare=function(){
        var win = $("#createShare_win");
        
        var params={};
        var title=$("#createShare_win input[name=title]").val();
        var content = $("#createShare_win textarea[name=content]").data("kendoEditor").value();
        var d0=$("#createShare_win select[name=province]").val();
        var d1=$("#createShare_win select[name=city]").val();
        var fields=shareAutoComplateWidget.getSelectedItems().join(",");
        fields=fields.split(",")
        
        params.title=title
        params.area={"d0":d0,"d1":d1}
        params.fields=fields
        params.content=content
        checkVarDic(params)
        
        nb.rpc.topicViews.c("createShare",params)
        .success(function(msg){
            nb.AlertTip.auto(msg);
        });
        
        nb.uiTools.closeEditDialogWin("#createShare_win");
    }   

    var setAwardVisual=function(){
        $("#createQuestion_win input[name=value]").hide();
        $("#scoreDtId").hide();
        $("#awardNumId").hide();
        $("#createQuestion_win select[name=aType]").bind("click",function(){
                var aType=$("#createQuestion_win select[name=aType]").val();
                if (aType !="不悬赏") {
                   $("#createQuestion_win input[name=value]").show();
                   $("#scoreDtId").show();               
                   if(aType=="积分") {
                       $("#awardNumId").show();
                   }else{
                       $("#awardNumId").hide();
                   }               
                }else{
                    $("#createQuestion_win input[name=value]").hide();
                    $("#scoreDtId").hide();
                    $("#awardNumId").hide();
                }
        });
    }     
    $(document).ready(function(){
        $("#postHelpLink").bind("click", function(){
            nb.uiTools.showEditDialogWin(null, "#createQuestion_win", {width:800, height:500});
            setAwardVisual();
        });
        
        $("#createShareDirect_btn").bind("click", function(){
            nb.uiTools.showEditDialogWin(null, "#createShare_win", {width:800, height:500});
        });
               
       $("#createQuestion_win .win_opbar button.ok").bind("click",function(){
            createQuestion();
        });
        
        $("#createShare_win .win_opbar button.ok").bind("click",function(){
            createShare();
        });
        
        nb.uiTools.setAreaSelect();
        questionAutoComplateWidget.__init__();
        shareAutoComplateWidget.__init__();
        
        $("#createQuestion_win textarea[name=content]").kendoEditor({});
        $("#createShare_win textarea[name=content]").kendoEditor({});
        
            var params={};
            nb.rpc.topicViews.c("getNewMessageNum",params)
            .success(function(msg){
                nb.AlertTip.auto(msg);
            });     
    });
})(jQuery);