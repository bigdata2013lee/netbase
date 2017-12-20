(function($){
	//前台用户中心的 我的动态、与我相关、设备动态三个页面的主JS文件【2014.12.19  jenny】
	//命名空间初始化
    var m = new nb.xutils.Observer();
    //定义提问窗体的技术领域下拉列表选择控件
    var  questionAutoComplateWidget = nb.BaseWidgets.extend("autoComplateWidget", {},{_panel_id:"#questionAutoComplateWidget"});
    //定义分享窗体的技术领域下拉列表选择控件
    var  shareAutoComplateWidget = nb.BaseWidgets.extend("autoComplateWidget", {},{_panel_id:"#shareAutoComplateWidget"});

    /**
	 * 验证提问或者分享数据
	 * @method _validateQtShParams
	 * @param {string} title 分享/提问标题
	 * @param {dic} area 服务地域
	 * @param {list} fields 技术领域
	 * @param {string} content 分享/提问内容
	 * @return {bool} 判断参数是否符合条件，返回一个提示信息
	 */
    var _validateQtShParams=function(params){
        var em = $(params.win).children(" div.validateErrorMsg");
        var rules = {
            title:function(val){return val.length<=20 && val.length >0},
            area:function(dic){
            		if(!dic["d0"]){return false}
            		else if(!dic["d1"]){return false}
            		else{ return true}
            	},
            fields:function(li){return li[0].length > 0},
            content:function(val){return val.length<=1000 && val.length >0}
        };
        var messages = {
            title:"请输入20字以内的标题",
            area:"请选择您所在区域的省份、城市",
            fields:"请选择话题所属的领域",
            content:"请输入1000字以内的内容"
        };
        var validator = new nb.xutils.Validator(em, rules, messages);
        return validator.validate(params);            
    };
    
    /**
	 * 验证提问或者分享数据
	 * @method _validateAward
	 * @param {string} award 提问悬赏
	 * @return {bool} 判断参数是否符合条件，返回一个提示信息
	 */
    var _validateAward = function(params){
        var em = $(params.win).children(" div.validateErrorMsg");
        var rules = {
    		award:function(dic){if(dic){
            	if(dic["aType"] == "人民币"){
            		if( /^0+/.test(dic["value"])){return false}
            	    else if(!/^[0-9]+$/.test(dic["value"])){return false}
            	    else{return true}
        	   }else if(dic["aType"] == "积分"){
            		var awardNum=$("#createQuestion_win span[name=awardNum]").text();
            		if(/^0+/.test(dic["value"])){return false}
            		else if(!/^[0-9]+$/.test(dic["value"])){return false}
            		else if(awardNum<=0 || awardNum < dic["value"]){return false}
            		else{return true}
            	}else{return true}
            }}
        };
        var messages = {
            award:"请输入有效悬赏"
        };
        var validator = new nb.xutils.Validator(em, rules, messages);
        return validator.validate(params);  
    }

    /**
	 * 定义并设置悬赏控件的事件
	 * @method setAwardVisual
	 */
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

    /**
	 * 提交提问数据
	 * @method createQuestion
	 * @param {string} verifyCode 验证码
	 * @return {bool} 判断参数是否符合条件，返回一个提示信息
	 * 1、先把所有参数获取
	 * 2、验证码通过Ajax的方式传到后台验证
	 * 3、验证码通过了，把数据通过Ajax方式提交到后台，返回一个信息
	 * 4、判断返回的信息如果为0，标示成功，否则失败，
	 * 5、若失败，弹出提示信息，并改变验证码
	 */
    var createQuestion=function(verifyCode){
        var params={};
        params.title=$("#createQuestion_win input[name=title]").val();
        params.content = $("#createQuestion_win textarea[name=content]").data("kendoEditor").value();
        params.area = {"d0":$("#createQuestion_win select[name=province]").val(),"d1":$("#createQuestion_win select[name=city]").val()};        
        params.fields=questionAutoComplateWidget.getSelectedItems().join(",").split(",");
        params.award={"aType":$("#createQuestion_win select[name=aType]").val(),"value":$("#createQuestion_win input[name=value]").val()}
        params.win = $("#createQuestion_win")
        
        if(_validateQtShParams(params) != true){return};
        if(_validateAward(params) != true){return};
        delete params.win;
        $.post("/ucenter/checkVerifyCode/",{verifyCode:verifyCode})
        .success(function(msg){
            if(msg=="0") {
                nb.rpc.topicViews.c("createQuestion",params)
                .success(function(msg){
                    nb.AlertTip.auto(msg);
                });        
            nb.uiTools.closeEditDialogWin("#createQuestion_win");
            }else{
                nb.AlertTip.auto("验证码错误");
                changeVerifyCode();
            }
        })
    }
    
    /**
	 * 提交分享数据
	 * @method createShare
	 * @param {string} verifyCode 验证码
	 * @return {bool} 判断参数是否符合条件，返回一个提示信息
	 * 1、先把所有参数获取
	 * 2、验证码通过Ajax的方式传到后台验证
	 * 3、验证码通过了，把数据通过Ajax方式提交到后台，返回一个信息
	 * 4、判断返回的信息如果为0，标示成功，否则失败，
	 * 5、若失败，弹出提示信息，并改变验证码
	 */
     var createShare=function(verifyCode){
        
        var params={};
        params.title=$("#createShare_win input[name=title]").val();
        params.content = $("#createShare_win textarea[name=content]").data("kendoEditor").value();
        params.area = {"d0":$("#createShare_win select[name=province]").val(),"d1":$("#createShare_win select[name=city]").val()};
        params.fields=shareAutoComplateWidget.getSelectedItems().join(",").split(",");
        params.win = $("#createShare_win") 
        
        if(_validateQtShParams(params) != true){return};
        delete params.win;
        $.post("/ucenter/checkVerifyCode/",{verifyCode:verifyCode})
        .success(function(msg){
            if(msg=="0") {
                nb.rpc.topicViews.c("createShare",params)
                .success(function(msg){
                    nb.AlertTip.auto(msg);
                });        
                nb.uiTools.closeEditDialogWin("#createShare_win");
            }else{
                nb.AlertTip.auto("验证码错误");
                changeVerifyCode();
            }
        })
    }  

    /**
	 * 改变显示的验证码，并清空验证码输入框
	 * @method changeVerifyCode
	 */
    var changeVerifyCode = function(){
        $("img[name=verifyCodeImg]").attr("src", "/getVerifyCode/?xtime=" + new Date().valueOf());
        $("input[name=verifyCode]").val("");
    }
    
    $(document).ready(function(){
    	
        changeVerifyCode();  
        
        // $("span[name=error_msg]").html("").hide();
        //触发改变验证码的事件
        $("a[name=changeVerifyCode]").bind("click", function(){ changeVerifyCode(); });
           
        //触发显示提问窗口事件和悬赏控件事件 
        $("#createQuestionDirect_btn").bind("click", function(){
            nb.uiTools.showEditDialogWin(null, "#createQuestion_win", {width:700, height:610});
            setAwardVisual();
        });
        
        //触发直接提问窗口显示时间
        $("#createShareDirect_btn").bind("click", function(){
            nb.uiTools.showEditDialogWin(null, "#createShare_win", {width:700, height:580});
        });
        
        //触发提交提问数据事件
        $("#createQuestion_win .win_opbar button.ok").bind("click",function(){
            var verifyCode=$("input[name=questionVerifyCode]").val();
            createQuestion(verifyCode);
        });
        
        //触发提交分享数据事件
        $("#createShare_win .win_opbar button.ok").bind("click",function(){
            var verifyCode=$("input[name=shareVerifyCode]").val();
            createShare(verifyCode);
        });
        
        //触发设备动态页面提问窗口显示，并把事件信息值赋给窗体控件
        $("button[name=createQuestion_btn]").bind("click", function(evt){
            setAwardVisual();
            var refMsg = $(this).closest("tr").find("td.evt_message_td").text();
            $("#createQuestion_win textarea[name=content]").data("kendoEditor").value('<pre class="ref_evt_msg">' + refMsg + '</pre><p></p>');
            nb.uiTools.showEditDialogWin(null, "#createQuestion_win", {width:700, height:610});
        });
        
        //触发设备动态页面分享窗口显示，并把事件信息值赋给窗体控件
        $("button[name=createShare_btn]").bind("click", function(evt){
            var refMsg = $(this).closest("tr").find("td.evt_message_td").text();
            $("#createShare_win textarea[name=content]").data("kendoEditor").value('<pre class="ref_evt_msg">' + refMsg + '</pre><p></p>');
            nb.uiTools.showEditDialogWin(null, "#createShare_win", {width:700, height:580});
        });
        
        //初始化技术地域下拉列表控件
        nb.uiTools.setAreaSelect();
        
        //初始化分享窗体和提问窗体服务领域控件
        questionAutoComplateWidget.__init__();
        shareAutoComplateWidget.__init__();
        
        //初始化分享窗体和提问窗体编辑器控件
        $("#createQuestion_win textarea[name=content]").kendoEditor({});
        $("#createShare_win textarea[name=content]").kendoEditor({});
    });
    
})(jQuery);