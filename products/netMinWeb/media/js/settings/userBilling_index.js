(function($) {
    var m = window.userBilling_index= new nb.xutils.Observer();
	var priceMap = {"Device": 20, "Website":10, "Network": 10, "Bootpo": 5, "ShortCutCmd":5};
      
    var toSelectModel = function(selectWidget2,selectVal){
    	selectWidget2.html("");
    	if(selectVal == "byYear"){
    		for(var i=1; i<4; i++){
    			var option = $(nb.xutils.formatStr('<option value="{0}">{1}</option>', i*12, i+"年"));
    			option.appendTo(selectWidget2);
    		}
    	}else{
    		for(var i=1; i<11; i++){
    			var option = $(nb.xutils.formatStr('<option value="{0}">{1}</option>', i, i+"个月"));
    			option.appendTo(selectWidget2);
    		}
    	}
    }; 
    
    
    var BaseBilling = {
    	
    	_panel_id: null,
    	billingType : null,
		save: function(){
			var self = this;
			var billingNum = $(self._panel_id + " input[name=billingNum]").val();
			var billingTime = $(self._panel_id + " .select2").val();
			var billingMoney = billingNum*billingTime*priceMap[self.billingType];
			var remoteParams = {
				billingType: self.billingType,
				billingNum:billingNum,
				billingTime:billingTime, 
				billingPrice: priceMap[self.billingType],
				billingMoney:billingMoney 
			};
			nb.rpc.billingViews.c("addBilling", remoteParams).success(function(msg){
				nb.AlertTip.auto(msg);
			});
		},
		
    	__init__: function(){
    		var self = this;
    		var billingNumEl = $(self._panel_id + " input[name=billingNum]");
    		var billingModelEl = $(self._panel_id + " .selectModel");
    		var billingTimeEl = $(self._panel_id + " .select2");
    		var billingMoneyEl = $(self._panel_id+" .li_money span[name=billingMoney]");
    		billingNumEl.val(1);
    		billingModelEl.val("byMonth");
			billingMoneyEl.html(priceMap[self.billingType]);
			
    		$(self._panel_id+" .panelContent").delegate("select,input", "change", function(){
    			if($(this).hasClass("selectModel")){
    				var selectVal = $(this).val();
    				toSelectModel(billingTimeEl, selectVal);
    			}
    			var billingNum = billingNumEl.val();
    			var billingTime = billingTimeEl.val();
				var billingSumMoney = billingNum*billingTime*priceMap[self.billingType];
				billingMoneyEl.html(billingSumMoney);
    		});
    		
  
    		$(self._panel_id + " li a[name=sumbitBt]").bind("click", function(){
    			if(billingNumEl.val() == 0){
    				alert("请选择购买个数！");
    				return;
    			}
    			if(!confirm("确定提交充值？")){return;}
    			self.save();
    			
    		});
    		
    		
    	}
    };


	m.deviceBilling = $.extend({}, BaseBilling, {
		_panel_id:"#panel_0001",
    	billingType : "Device"	
	});    
    
    
	m.websiteBilling = $.extend({}, BaseBilling, {
		_panel_id:"#panel_0002",
    	billingType : "Website"	
	});
	
	m.networkBilling = $.extend({}, BaseBilling, {
		_panel_id:"#panel_0003",
    	billingType : "Network"		
	});
	
	m.bootpoBilling = $.extend({}, BaseBilling, {
		_panel_id:"#panel_0004",
    	billingType : "Bootpo"	
	});
	
	m.shortCutCmdBilling = $.extend({}, BaseBilling, {
		_panel_id:"#panel_0005",
    	billingType : "ShortCutCmd"		
	});
	
	
	//----------------------------------------------------------------------------------------
	
    var _conditions = {"userId": userId};
    var _ds = null;
    var getDs = m.getDs = function() {
        if(_ds) return _ds;
        var ds = new kendo.data.DataSource({
            type : "json", pageSize : 50,
            transport : {
                read : nb.rpc.billingViews.rc("listBillingsByUser"),
                parameterMap: function(){
                  if (! _conditions) return;
                  return  {
                      params : $.toJSON(_conditions)
                  }
                },
            }
    
        });
        _ds = ds;
        return _ds;
    };
	
	
    m.createGrid = function() {
        
        var onChange=function(arg){
            //pass
        };
 
        var _columns = [
            { field : "_id", title : "编号",  width : 200},
            { field : "type", title : "类型", width : 80, template: "#=nb.Render.zh(type)#" },
            { field : "startTime", width:120, title : "购买时间", template : "#=nb.xutils.getTimeStr(startTime * 1000, true)#"},
            { field : "endTime", width:120, title : "过期时间", template : "#=nb.xutils.getTimeStr(endTime * 1000, true)#"},
            { field : "count", title : "购买个数", width:80},
            { field : "usedCount", title : "已用个数", width:80},
            { field : "totalPrice", title : "总价", width:80, template : "#=nb.xutils.showMoney(totalPrice)#"},
			{ field : "isvalid", title : "状态", width:80, template: '#=nb.Render.zh(isvalid,{"true":"有效", "false":"无效"})#' },

        ];

        $("#data-grid").kendoGrid({
            dataSource : getDs(),
            change:onChange,
            height : 400,
            pageable:true,
            sortable : true,
            columns : _columns
        });

        return $("#data-grid").data("kendoGrid");
    };
	
    
    $(document).ready(function(){
    	$("#user_left_menus a").bind("click", function(){
    		var actionName = $(this).attr("name");
    		$(".panel.swich").hide();
    		$(".panel.swich[actionName=" + actionName + "]").show();
    		if(actionName == "listBillings"){
    			getDs().read();
    			m.createGrid();
    			
    		}else{
    			nb.uiTools.commLoading.insertTo("body", "");
    			setTimeout(function(){
    				nb.uiTools.commLoading.cancel("body");
    			}, 200);
    		}
    	});
    	
    	$(".numberStyle input[name=billingNum]").kendoNumericTextBox();
    	
    	m.deviceBilling.__init__();
    	m.websiteBilling.__init__();
    	m.networkBilling.__init__();
    	m.bootpoBilling.__init__();
    	m.shortCutCmdBilling.__init__();
    	
    });

})(jQuery);
