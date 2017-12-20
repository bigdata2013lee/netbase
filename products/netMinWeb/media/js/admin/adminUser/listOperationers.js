(function($){
	//后台管理中心的运维商页面的主JS文件 【2014.12.19  jenny】	
	var m = new nb.xutils.Observer();
	//定义一个技术领域下拉列表控件
	var autoComplateWidget1 = nb.BaseWidgets.extend("autoComplateWidget",{},{_panel_id:"#autoComplateWidget1"});
	//定义一个服务地域下拉列表控件
	var autoComplateWidget2 = nb.BaseWidgets.extend("areaAutoComplateWidget",{},{_panel_id:"#areaAutoComplateWidget",_data:window.nb_areas2,_max:4});
  
    /**
	 * 验证新添加的运维商的数据
	 * @method _validateBaseInfoParams
	 * @param {string} originalName 运维商名称
	 * @param {string} email 运维商联系邮箱
	 * @param {string} username 运维商账号
	 * @param {string} password 运维商账号密码
	 * @param {string} companyName 公司名称
	 * @param {string} bussinessLicenseNum 营业执照
	 * @param {string} phoneNum 联系电话
	 * @param {string} address 联系地址
	 * @return {bool} 返回bool值，并且如果为false还会弹出提示消息
	 */
	var _validateBaseInfoParams=function(params){
		var em = $("#addOperationWin div.validateErrorMsg");
		var rules = {
		    originalName:"required",
		    email:"email",
		    username:"email",
		    password:"required",
		    companyName:"required",
		    bussinessLicenseNum:"required",
		    phoneNum:{method: "regex", exp: /((\d{11})|^((\d{7,8})|(\d{4}|\d{3})-(\d{7,8})|(\d{4}|\d{3})-(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})|(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1}))$)/},
		    address:"required"
		};
		var messages = {
		    originalName:"用户名必填",
		    email:"请填写一个正确的邮箱格式",
		    username:"请填写一个正确的邮箱格式",
		    password:"用户登录密码必填",
		    companyName:"公司名称必填",
		    bussinessLicenseNum:"公司营业执照编号必填",
		    address:"公司地址必填",
		    phoneNum:"联系电话格式不对"
		};
		var validator = new nb.xutils.Validator(em, rules, messages);
		return validator.validate(params);            
	};
    
    /**
	 * 提交新添加的运维商的数据
	 * @method _validateBaseInfoParams
	 * @return {string} 数据验证成功，通过Ajax把参数传到后台，返回一个成功与否的提示消息
	 */
    var editOperationerInfo = function(){        
        var params=nb.uiTools.mapFields("#addOperationWin");
        params.technologyFileds = autoComplateWidget1.getSelectedItems();
        params.serviceAreas = autoComplateWidget2.getSelectedItems();
        
        if(!_validateBaseInfoParams(params)){return;}
        
        nb.rpc.adminUserViews.c("addOperation", params)
        .success(function(msg){
            nb.AlertTip.storeCookie(msg);
            nb.uiTools.closeEditDialogWin("#addOperationWin");
            location.reload();
        });
    }

   
    $(document).ready(function() {
    	//触发查询运维商的事件
        $("div.query_tool_bar input[name=search]").bind("click",function(){
            var operationer = $("div.query_tool_bar input[name=operationer]").val();
              window.location.href = "/admin/listOperationers/?operationer="+ operationer;
        })
        
        //触发添加运维商的窗体显示事件
        $("div.query_tool_bar a[name=addOperation]").bind("click",function(){            
            nb.uiTools.showEditDialogWin(null, "#addOperationWin", {width:730, height:650});
        })
        
        //触发提交运维商数据的事件
        $("#addOperationWin .win_opbar button.ok").bind("click",function(){
            editOperationerInfo();
        });        
		
		//触发删除运维商的事件，返回操作是否成功的信息，并重新加载页面
        $("table.data_table tbody tr td a[action=delete]").bind("click",function(){
        	var params ={opId:$(this).attr("dataId")} 
            if(window.confirm("您确定要删除吗？")){
	        	nb.rpc.adminUserViews.c("delOpertioner", params)
		        .success(function(msg){
		            nb.AlertTip.storeCookie(msg);
		            location.reload();
        		});
            }else{
            	return;
            }
        })
        
        //初始化技术领域下拉列表控件
        autoComplateWidget1.__init__();
		//初始化服务地域下拉列表控件
        autoComplateWidget2.__init__();
    });    
    
})(jQuery);
