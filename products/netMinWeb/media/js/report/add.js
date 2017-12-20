(function($){
    var m = window.Index = new nb.xutils.Observer();
    m.currentDevId = window.moUid;
    var reportlist = {DeviceClass:["cpu,mem,disk,availability,event,"],
    		NetworkClass:["cpu,mem,disk,curConn,newConn,availability,event,"],
    		WebSiteClass:["availability,resTime,event,"]};

    reportListTree.on("selectOrgNode",function(orgUid, uname){
        window.location.href = "/report/content/"+orgUid;
    });
	//===报表对象基类===
    editreportBaseWidget = {
        _sources:{
        	exportFormats:[{text:"PDF格式", val:"pdf"}, {text:"JPG格式", val:"jpg"},
        	 {text:"PNG格式", val:"png"}],        	 
        	 defaultTimes:[{text:"一天内",val:"day"},{text:"三天内",val:"3day"},{text:"一周内",val:"week"},{text:"一月内",val:"month"}],
           changereportType:function(e){
                var panel = $(e.target).closest("div.panelContent");
                var widget = panel.data("nbWidget");
                widget._selectReportType(this.reportType);
            }         
        },
        _data:{
            description:"",
            reportType:['DeviceClass','WebSiteClass'],
            //reportType:['DeviceClass','WebSiteClass','NetworkClass'],
            exportFormat:"pdf",
            email:"",timeRange:"0",
            defaultTime:"day",startTime:"2012/10/22",endTime:"2013/01/09",
            reports:["cpu","mem","disk","curConn","newConn","availability","event","resTime"],
            filterCondition:{}
        },
        _render:function(){
            var self = this;
            //self._data.enable = nb.xutils.val2booleanStr(self._data.enable);
            self.viewModel = kendo.observable($.extend({}, self._data, self._sources));
            kendo.bind($(self._panel_id), self.viewModel);
            self._selectReportType(self.viewModel.reportType);
        },
        _selectReportType:function(){
        	 //_selectReportType method in base.
        },
        save: function(){
            //save method in base.
        },
        _validate:function(params){
            var self = this;
            var errorEl = $(self._panel_id + " div.validateErrorMsg");
            var rules = {
            	exportFormat: function(exportFormat){
                    if(params.exportFormat.length > 0) return true;
                    return false;
                },
                filterCondition: function(filterCondition){
                    if('DeviceClass' in filterCondition) return true;
                    if('WebSiteClass' in filterCondition) return true;
                    if('NetworkClass' in filterCondition) return true;
                    return false;
                },
                description:"required",
            	toMail:"required",
            };
            var messages = {"description": "报表名称为必填项","toMail": "邮件收件人为必填项","exportFormat":"至少选择一个报表导出类型","filterCondition":"至少选择一个报表类型"};
            
            var rules2 = {            
            	toMail:function(toMail){
            		var result = true;
            		for(var j=0;j<toMail.length;j++){
		            	if(toMail[j].length >0)
		            	{
		            		var reg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
							if(!reg.test(toMail[j])){
								result = false;
								return;
							}
		            	}
		            }  
		            return result;    
               },
                filterCondition: function(filterCondition){
                	if(params.filterCondition["DeviceClass"]!=null && params.filterCondition["DeviceClass"].reports.length >0)return true;
                	if(params.filterCondition["WebSiteClass"]!=null && params.filterCondition["WebSiteClass"].reports.length >0)return true;
                	if(params.filterCondition["NetworkClass"]!=null && params.filterCondition["NetworkClass"].reports.length >0)return true;
                	return false;
                },                
                objectClass: function(filterCondition){
                	if(params.filterCondition["DeviceClass"]!=null && params.filterCondition["DeviceClass"].objClass.length >0&&params.filterCondition["DeviceClass"].objClass[0].length >0)return true;
                	if(params.filterCondition["WebSiteClass"]!=null && params.filterCondition["WebSiteClass"].objClass.length >0 &&params.filterCondition["WebSiteClass"].objClass[0].length >0)return true;
                	if(params.filterCondition["NetworkClass"]!=null && params.filterCondition["NetworkClass"].objClass.length >0&&params.filterCondition["NetworkClass"].objClass[0].length >0)return true;
                	return false;
                },
                timeRange: function(timeRange){
                	if(timeRange.customTime){
                		if(timeRange.customTime.startTime ==null||timeRange.customTime.startTime.length==""){
                			return false;
                		}
                		if(timeRange.customTime.endTime ==null||timeRange.customTime.endTime.length==""){
                			return false;
                		}
                	}
                	else if(timeRange.defaultTime ==null||timeRange.defaultTime.length==""){
                			return false;
                	}
                	return true;
                }
            };
            var messages2 = {"toMail": "请输入正确的邮件收件人","filterCondition": "至少选择一个报表内容","objectClass": "请选择报表数据过滤","timeRange":"请选择正确的时间"};
            
            var validator = new nb.xutils.Validator(errorEl, rules, messages);
            var validator2 = new nb.xutils.Validator(errorEl, rules2, messages2);
            
            var vrs1 = validator.validate(params);
            if(vrs1 == false) return false;
            return validator2.validate(params);
        },      
        reload:function(){
            var self = this;
            self._render();
        },
        display: function(fg){
            var self = this;
            if(fg){ $(self._panel_id).show(); return;}
            $(self._panel_id).hide();
        },
        __init__:function(){
            var self = this;
            $(self._panel_id).data("nbWidget", this);
            self.reload();         
            $(self._panel_id + " div.op_bar input[name=save]").bind("click", function(){
                self.save();
            });
        }           
    };
    //===创建自定义报表===
    m.createreportWidget = $.extend({}, editreportBaseWidget, {
        _panel_id: "#createreportWidget",
        _selectReportType: function(reportType){
            var self = this;
            var box = $(self._panel_id);
	        box.find(".network_reports").hide();
	        box.find(".website_reports").hide();
	        box.find(".device_reports").hide();
	        box.find("#report_device_tree").hide();
	        box.find("#report_website_tree").hide();
	        box.find("#report_network_tree").hide();
            for(var j=0;j<reportType.length;j++){
            	if(reportType[j] === "DeviceClass"){
	            	box.find(".device_reports").show();
	            	box.find("#report_device_tree").show();
	            }
	            if(reportType[j] === "WebSiteClass"){
	            	box.find(".website_reports").show();
	            	box.find("#report_website_tree").show();
	            }
	            if(reportType[j] === "NetworkClass"){
	            	box.find(".network_reports").show();
	            	box.find("#report_network_tree").show();
				}
            }          
        },
        save: function(){
            var self = this;
            var pobj = GetParams(self.viewModel);
            if(!self._validate(pobj)) return;
            nb.rpc.reportApi.c("addReportRule", {medata:pobj}).
            success(function(msg){
                nb.AlertTip.storeCookie(msg);
				window.location.href="/report/index";
            });
        }
    });  
    
    //===组装数据对象===
    function GetParams(ViewModel){
		var params={
			description:ViewModel.description,
	        exportFormat:ViewModel.exportFormat,
	        toMail:ViewModel.email.split(";"),
	        timeRange:{},
	        filterCondition:{}
		};
		try
		{
			if(ViewModel.timeRange =="0"){
				params.timeRange = {defaultTime:ViewModel.defaultTime};
			}else{
				params.timeRange = {customTime:{startTime: kendo.toString(ViewModel.startTime, 'd'),endTime: kendo.toString(ViewModel.endTime, 'd')}};
			}
			for(var j=0;j<ViewModel.reportType.length;j++){
				e = ViewModel.reportType[j];
				var obj = $("#"+e+"ID");
				var hiddenid = obj!=null?obj.val().split(","):[];
				params.filterCondition[ViewModel.reportType[j]] = {reports:GetArray(ViewModel.reports, ViewModel.reportType[j]),objClass:hiddenid};
			}
		}
		catch(err)
		{
			console.info(err);
		}
		return params;
	}
    function GetArray(arr, name){
    	var array = [];
    	var relist = reportlist[name];
    	if(!relist||relist.count==0){return array;}
    	for(var j=0;j<arr.length;j++){
    		if(relist[0].indexOf(arr[j]+",")>-1){
    			array.push(arr[j]);
    		}
    	}
    	return array;
    }
    //===初始化日期控件===
    var initDateUi = function(){
        function startChange() {
            var startDate = start.value(), endDate = end.value();

            if (startDate) {
                startDate = new Date(startDate);
                startDate.setDate(startDate.getDate());
                end.min(startDate);
            } else if (endDate) {
                start.max(new Date(endDate));
            } else {
                endDate = new Date();
                start.max(endDate);
                end.min(endDate);
            }
        }

        function endChange() {
            var endDate = end.value(), startDate = start.value();

            if (endDate) {
                endDate = new Date(endDate);
                endDate.setDate(endDate.getDate());
                start.max(endDate);
            } else if (startDate) {
                end.min(new Date(startDate));
            } else {
                endDate = new Date();
                start.max(endDate);
                end.min(endDate);
            }
        }
        var start = $(".start").kendoDatePicker({ change : startChange  }).data("kendoDatePicker");
        var end = $(".end").kendoDatePicker({ change : endChange }).data("kendoDatePicker");
        var _v = 604800000; //7天毫秒数
                
        start.value(new Date(new Date().valueOf() - _v));
        end.value(new Date());
        start.min(new Date(new Date().valueOf() - _v * 4 * 12));
        start.max(end.value());
        end.min(start.value()); 
        end.max(new Date());           
        if(window.eventConsoleFor == "events"){
            start.value(null);
            end.value(null);
        }
    };
    $(document).ready(function(){
        initDateUi();
        m.createreportWidget.__init__();
    });
})(jQuery);
