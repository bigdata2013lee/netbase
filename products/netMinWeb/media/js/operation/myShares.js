(function($){
	//运维商用户中心的我的资料的我要分享页面的主JS【2014.12.18  jenny】	
    var m = new nb.xutils.Observer();

	//定义一个技术类别下拉框控件
    var  shareAutoComplateWidget = nb.BaseWidgets.extend("autoComplateWidget", {},{_panel_id:"#shareAutoComplateWidget"});
    
    /**
	 * 验证我要分享的数据，
	 * @method _validateShareParams
	 * @param {string} title 分享标题
	 * @param {dic} area 服务地域
	 * @param {list} fields 技术领域
	 * @param {string} content 分享内容
	 * @return {bool} 判断参数是否符合要求
	 */
    var _validateShareParams = function(params){
        var em = $("#createShare_win div.validateErrorMsg");
        var rules = {
            title:function(val){return val.replace(/\s/ig,'').split("<p></p>").join("").length<=20 && val.replace(/\s/ig,'').split("<p></p>").join("").length >0},
            area:"required",
            fields:"required",
            content:function(val){return val.replace(/\s/ig,'').split("<p></p>").join("").length<=1000 && val.replace(/\s/ig,'').split("<p></p>").join("").length >0}
        };
        var messages = {
            title:"请输入20字以内的标题",
            area:"请选一个具体的地区",
            fields:"请选择技术领域",
            content:"请输入1000字以内的内容"
        };
        var validator = new nb.xutils.Validator(em, rules, messages);        
        return validator.validate(params);          
    };
    
    /**
	 * 提交我要分享的数据，
	 * @method createShare
	 * @return {string} 在参数都通过验证后，通过Ajax的方式提交，返回提交成功与否的提示信息，并关闭窗体
	 */
     var createShare = function(){
        var params={};
        
        params.title=$("#createShare_win input[name=title]").val();
        params.content=$("#createShare_win textarea[name=content]").data("kendoEditor").value();
        params.area={"d0":$("#createShare_win select[name=province]").val(),"d1":$("#createShare_win select[name=city]").val()}
        params.fields=shareAutoComplateWidget.getSelectedItems();
        
        if(!_validateShareParams(params))return;
        nb.rpc.topicViews.c("createShare",params)
        .success(function(msg){
            nb.AlertTip.storeCookie(msg);
        	nb.uiTools.closeEditDialogWin("#createShare_win");
            location.reload();
        });
        
    }   
    
    
    $(document).ready(function(){
    	//触发我要分享的窗体弹出事件
        $("div.op_bar a[action=createShare]").bind("click", function(){
            nb.uiTools.showEditDialogWin(null, "#createShare_win", {width:700, height:500});
        });
                
        //触发提交我要分享的数据的事件
        $("#createShare_win .win_opbar button.ok").bind("click",function(){
            createShare();
        })
        
        //初始化一个省市级联选择控件
        nb.uiTools.setAreaSelect();
        
    	//初始化一个技术类别下拉框控件
        shareAutoComplateWidget.__init__();
        
        //初始化一个kendoUI的编辑器控件
        $("#createShare_win textarea[name=content]").kendoEditor({});
    });
})(jQuery);
