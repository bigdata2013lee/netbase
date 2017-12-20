(function($){
	//运维商用户中心服务合约页面的请求扩充设备js【2014.12.18  jenny】
	
    /**
	 * 获取根据用户输入的设备扩充数得到的金额
	 * @method getPrice
	 * @param {string} counts 设备扩充数
	 * @return {string} 返回金额字符串或者提示字符串
	 */
    var getPrice = function(counts){
        if(counts.length <10){
            var count = parseInt(counts)
            if(count){
                if(count < 10){return "最少购买十台！"}
                else if(count <= 100){return  (count*4*0.9).toFixed(2)}
                else if(count >100 && count <= 500){return  (count*4*0.8).toFixed(2)}
                else{return  (count*4*0.5).toFixed(2)}            
            }else if(count == 0){
            	return count;
            }else{
                return "请输入要购买的数字"
            }
        }else{
            return "请输入十位数以内的数字"
        }
    }
    
    /**
	 * 获取一个float类型的数字
	 * @method getInt
	 * @param {string} val 字符串
	 * @return {string} 返回float类型的数字或者0
	 */
    var getInt = function(val){
        if(parseInt(val)){return parseFloat(val)}else{return 0}
    }
    
    /**
	 * 验证用户输入的社扩充数是否符合
	 * @method validateParam
	 * @param {string} val 设备扩充数
	 * @param {string} str “主机”/“站点”/"网络"
	 * @return {bool} 返回一个bool类型的值
	 */
    var validateParam = function(val,str){
    	if(val == "0"){return true;}
        if (!/^[0-9]+$/.test(val)) {nb.AlertTip.auto("warn:" + str + "数目只能为非负数");return false}
        else if(/^0/.test(val)){nb.AlertTip.auto("warn:请输入有效" + str + "数目");return false}
        else if(val.length >10 ){nb.AlertTip.auto("warn:请输入10位数以内的要扩充的"+ str +"数");return false}
        else if(parseInt(val) >0 && parseInt(val) < 10){nb.AlertTip.auto("warn:最少购买十台" + str );return false}
        else { return true};
    }
    
    /**
	 * 用户在输入设备扩充数的时候显示相应的金额信息
	 * @method inputKeyup
	 */
    var inputKeyup = function(evt){
        var hostPr = getPrice($("#extendDevicePage div dl dd input#host").val());
        var websitePr = getPrice($("#extendDevicePage div dl dd input#website").val());
        var networkPr = getPrice($("#extendDevicePage div dl dd input#network").val());
        
        var price =  getPrice(evt.val());
        var totalPr = parseInt(getInt(hostPr))+ parseInt(getInt(websitePr)) + parseInt(getInt(networkPr));
        $("#extendDevicePage div dl.total_price").css("display","block").find("em.total_price").html( totalPr.toFixed(2) +" RMB");              
        if (parseInt(price)){
            evt.siblings("em").html(getInt(price).toFixed(2)  +" RMB");            
        }else{
            evt.siblings("em").html(price);
        }    
    } 
    
    /**
	 * 提交用户的设备扩充数据
	 * @method extendDevice
	 * 在数据验证通过之后，通过Ajax的方式提交，提交成功，返回一个字符串，并关闭窗体
	 */
    var extendDevice = function(){
        var params={};
        var host=$("#host").val();              
        var website=$("#website").val();                  
        var network=$("#network").val();
        if(!validateParam(host,"主机")){return};   
        if(!validateParam(website,"站点")){return};    
        if(!validateParam(network,"网络") ){return};   

		money = parseFloat(getPrice(host)) + parseFloat(getPrice(website)) + parseFloat(getPrice(network));

    	if(money == 0){
    		nb.AlertTip.auto("warn:请至少购买一种");
    		return;
    	}
            
        params.host = host;
        params.website=website;
        params.network=network;
        nb.rpc.operationView.c("extendDevice",params)
        .success(function(msg){
            nb.AlertTip.auto(msg);
            nb.uiTools.closeEditDialogWin("#extendDevicePage");
        }); 
    }

    $(document).ready(function(){
		//触发设备扩充窗体弹出的事件
        $("a[name=extend_device]").bind("click", function(){
            nb.uiTools.showEditDialogWin(null, "#extendDevicePage",{width:440, height:300});
        })
        
        //触发设备扩充数据提交事件
        $("#extendDeviceBtk").bind("click",function(){
             extendDevice();
        })       
         
        //触发输入时显示相应金额信息的事件
        $("#extendDevicePage div dl dd input").bind("keyup",function(){
			inputKeyup($(this));
        })
    });
})(jQuery)


