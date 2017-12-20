(function($){
    //运维商为自己的客户添加设备【2014.12.18  jenny】
    
    /**
	 * 验证输入的数据是否合法
	 * @method validateParam
	 * @param {string} 
	 * @return {bool} 判断参数是否符合
	 */
    var validateParam = function(val,str){
        if(val == "0"){return true;}
        if (!/^[0-9]+$/.test(val)) {nb.AlertTip.auto("warn:" + str + "数目只能为非负数");return false}
        else if(/^0/.test(val)){nb.AlertTip.auto("warn:请输入有效" + str + "数目");return false}
        else if(val.length >10 ){nb.AlertTip.auto("warn:请输入10位数以内的要扩充的"+ str +"数");return false}
        else { return true};
    }
    
    /**
	 * 验证输入的设备扩充数是否在运维商可用设备数范围内
	 * @method checkEnough
	 * @param {string} wantNum 扩充设备数
	 * @param {string} availableNum 可用设备数
	 * @return {bool} 判断参数是否符合
	 */
    var checkEnough=function(wantNum,availableNum){
        if(parseInt(wantNum)-parseInt(availableNum)<=0){
            return false;
        }else{
            return true;
        }
    }
    
    //提交设备扩充数据，验证未通过，返回提示字符串，否则通过API将数据提交到后台，反映到数据库，关闭窗体，返回提交成功数据
    var extendDevice = function(){
        var params={};
        var userid=$("#userid").val();
        var host=$("#host").val();
        var website=$("#website").val();
        var network=$("#network").val();
        
        var availableHost=$("#available_host").html();
        var availableWebsite=$("#available_website").html();
        var availableNetwork=$("#available_network").html();
        
        if(!validateParam(host,"主机")){return};   
        if(!validateParam(website,"站点")){return};    
        if(!validateParam(network,"网络") ){return};   
        if(host=="0" && website=="0" && network=="0"){nb.AlertTip.auto("请至少选择一种需要扩充的设备类型");return}
        if(checkEnough(host,availableHost)){nb.AlertTip.auto("可用主机数不足，请添加，谢谢");return}
        if(checkEnough(website,availableWebsite)){nb.AlertTip.auto("可用站点数不足，请添加，谢谢");return}
        if(checkEnough(network,availableNetwork)){nb.AlertTip.auto("可用网络设备数不足，请添加，谢谢");return}
        params.host=host;
        params.website=website;
        params.network=network;
        params.userid=userid;
        nb.rpc.operationView.c("extendDeviceByOperationer",params)
        .success(function(msg){
            nb.AlertTip.auto(msg);
            nb.uiTools.closeEditDialogWin("#extendDevicePage");
        }); 
    }
    
    
    $(document).ready(function(){
		//触发显示添加设备的窗体的事件
        $("a[name=extend_device]").bind("click", function(){
        	var userid=$(this).attr("userid");
        	$("#userid").val(userid);
            nb.uiTools.showEditDialogWin(null, "#extendDevicePage",{width:440, height:280});
        })
        
        //触发提交设备数据的事件
        $("#extendDeviceBtk").bind("click",function(){
             extendDevice();
        })

        
    });
})(jQuery)


