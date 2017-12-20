(function($){
	//运维商用户中心的我的资料界面的主JS【2014.12.18  jenny】
    var m = new nb.xutils.Observer();
    
    //定义一个技术领域的下拉列表控件
    var autoComplateWidget1 = nb.BaseWidgets.extend("autoComplateWidget",{},{_panel_id:"#autoComplateWidget1"});
    //定义一个服务地域下拉列表控件
    var autoComplateWidget2 = nb.BaseWidgets.extend("areaAutoComplateWidget",{},{_panel_id:"#areaAutoComplateWidget",_data:window.nb_areas2,_max:4});
    
    /**
	 * 验证我的资料数据，
	 * @method _validateBaseInfoParams
	 * @param {string} companyName 公司名称
	 * @param {string} bussinessLicenseNum 营业执照
	 * @param {string} phoneNum 联系电话
	 * @param {string} address 地址
	 * @param {string} technologyFileds 技术领域
	 * @param {string} technologyForte 技术特长
	 * @param {string} serviceAreas 服务地域
	 * @return {bool} 判断数据是否符合，返回布尔值
	 */
    var _validateBaseInfoParams = function(params){
        var em = $("#editPersonalInfoWin div.validateErrorMsg");
        var rules = {
            companyName:"required",
            bussinessLicenseNum:"required",
            phoneNum:"phone",
            address:"required",
            technologyFileds:"required",
            technologyForte:"required",
            serviceAreas:"required"
        };
        var messages = {
            companyName:"公司名称必填",
            bussinessLicenseNum:"公司营业执照编号必填",
            address:"公司地址必填",
            phoneNum:"联系电话格式不对",
            technologyFileds:"技术领域为必填项",
            technologyForte:"技术特长为必填项",
            serviceAreas:"服务领域为必填项"
        };
        var validator = new nb.xutils.Validator(em, rules, messages);
        return validator.validate(params);            
    };
    
    /**
	 * 提交我的资料数据，
	 * @method _validateBaseInfoParams
	 * @return {string} 如果数据通过验证，那么通过Ajax的方式提交数据到后台，返回成功与否的信息，并关闭窗体，刷新页面
	 */
    var editPersonalInfo = function(){        
        var params=nb.uiTools.mapFields("#editPersonalInfoWin");
        
        params.technologyForte = $("#editPersonalInfoWin input[name=technologyForte]").val();
        params.technologyFileds = autoComplateWidget1.getSelectedItems();
        params.serviceAreas = autoComplateWidget2.getSelectedItems();
        params.icon = $("#editPersonalInfoWin img").attr("src");
        if(!_validateBaseInfoParams(params)){return;}
        nb.rpc.operationView.c("editPersonalInfo", params)
        .success(function(msg){
            nb.AlertTip.storeCookie(msg);
            nb.uiTools.closeEditDialogWin("#editPersonalInfoWin");
            location.reload();
        });
    }

    
    
    $(document).ready(function(){
        //触发编辑我的资料的窗体弹出事件
        $("h3.info_header a[action=editPersonalInfo]").bind("click",function(){       
            nb.uiTools.showEditDialogWin(null, "#editPersonalInfoWin", {width:800, height:650, title:"用户资料修改申请"});         
        })
        
        //触发提交我的资料数据的事件
        $("#editPersonalInfoWin .win_opbar button.ok").bind("click",function(){
            editPersonalInfo();
        });
        
        //触发编辑个人头像的窗体弹出事件
        $("#editPersonalInfoWin a[action=selectIcon]").bind("click",function(){
            nb.uiTools.showEditDialogWin(null, "#user_icons_select_div_win", {width:640, height:300, title:"选择头像"});         
        })
        
        //触发点击图片便选中头像并关闭弹窗事件
        $("#user_icons_select_div_win img").bind("click",function(){
			var src = $(this).attr("src");
			$("#editPersonalInfoWin img").attr("src",src);
			nb.uiTools.closeEditDialogWin("#user_icons_select_div_win");
        })
        
        //技术领域的下拉列表控件的初始化
        autoComplateWidget1.__init__();
        //服务地域下拉列表控件的初始化
        autoComplateWidget2.__init__();
            
    });
    
})(jQuery);
