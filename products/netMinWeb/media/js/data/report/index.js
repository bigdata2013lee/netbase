(function($){
	var imgsRealPath = "/opt/netbase4/nbfiles/imgs/";
    var m = window.Index = new nb.xutils.Observer();
    m.currentDevId = window.moUid;
    reportListTree.on("selectOrgNode",function(orgUid, uname){
    	if(orgUid !== "0"){
        	window.location.href = "/report/content/"+orgUid;
       }
    });
    
    m.on("afterViewInfoWidgetReload", function(){
    });
    var reportlist = {DeviceClass:["cpu,mem,disk,availability,event,"],
    		NetworkClass:["cpu,mem,disk,curConn,newConn,availability,event,"],
    		WebSiteClass:["availability,resTime,event,"]};
   
	//===报表对象基类===
    editreportBaseWidget = {
    	_panel_contentid: "#reportContentWidget",
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
        _data:null,
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
        delReport:function(){},
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
            var messages2 = {"toMail": "请输入正确的邮件收件人","filterCondition": "请选择报表内容","objectClass": "请选择报表数据过滤","timeRange":"请选择正确的时间"};
            
            var validator = new nb.xutils.Validator(errorEl, rules, messages);
            var validator2 = new nb.xutils.Validator(errorEl, rules2, messages2);
            
            var vrs1 = validator.validate(params);
            if(vrs1 == false) return false;
            return validator2.validate(params);
        },
        reload:function(){
            var self = this; 
            
            nb.rpc.reportApi.c("getReportRule", {uid:rUid}).success(function(data){
            	//模拟数据
            	var remotedata = {
		            description:"本周性能报表",exportFormat:"pdf",toMail:["admin@gmail.com","ttt@ttt.com"],
		            timeRange:{defaultTimes:"week"},filterCondition:{
		            DeviceClass:{
		            	reports:["cpu","mem"],
		            	objClass:["530daa849c591543751506b1","530daa729c591543751506af","530daa599c591543751506ad","530da99e9c5915432a7b909b"]},
		            WebSiteClass:{reports: ["availability","event"],
		            objClass: ["530daac19c591543751506b4","530daad49c591543751506b5"]},
		            NetworkClass:{reports: ["availability","event"],
		            objClass:["530efa849c591517f14ead3f","530efa849c591517f14ead43","530efa849c591517f14ead44","530efa849c591517f14ead42","530efa849c591517f14ead45","530efa849c591517f14ead4a","530efa849c591517f14ead4c","530efa849c591517f14ead4d"]}}
		        };
		        $(".panelTitle").html(data.description);
                self._data = GetData(data);
                self._render();
            });
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
            
            $(self._panel_id + " div.op_bar input[name=del]").bind("click", function(){
                self.delReport();
            });
        }           
    };
   
    m.reportContentWidget = {
    	_sources:{},
    	_panel_id:"#reportContentWidget",
    	_data:null,
    	_render:function(){
            var self = this;
            //var template = self.getTemplate();
            //$(self._panel_id + " .box:first").html(template(self._data)); 
            var detailhtml = []; 
            detailhtmlwidget(self._data.cpu,"#detail_cpu_table","#detail_cpu_photo","#detail_cpu","cpu");
            detailhtmlwidget(self._data.mem,"#detail_mem_table","#detail_mem_photo","#detail_mem","mem");
            detailhtmlwidget(self._data.resTime,"#detail_resTime_table","#detail_resTime_photo","#detail_resTime","resTime");
            detailhtmlwidget(self._data.availability,"#detail_availability_table","#detail_availability_photo","#detail_availability","availability");
            if (self._data.disk&&self._data.disk[0]) {
            	var table = [];
	            table.push("<table width='85%' class='tabChart' border='0' cellspacing='0' cellpadding='0'><tr><td class='tb01'>设备</td><td class='tb01'>分区大小</td><td class='tb01'>已用空间</td><td class='tb01'>利用率%</td></tr>");
	            var datavalue;
	            var classname;
	            for (var i = 0; i < self._data.disk.length; i++) {
	            	if(i%2==0){classname="tb02";}
	            	else{classname=="tb03";}
	                table.push("<tr><td class='"+classname+"'>" + self._data.disk[i].title + "</td><td class='"+classname+"'>"+ self._data.disk[i].capacity +"</td><td class='"+classname+"'>"+ self._data.disk[i].usedCapacity +"</td>");
	                table.push("<td class='"+classname+"'>" + self._data.disk[i].utilization +"</td></tr>");
	            }
	            table.push("</table>");
	            $("#detail_disk_table").html(table.join(""));
            }
            else{
	        	$("#detail_disk").hide();
            }
            if (self._data.event&&self._data.event.length ==2) {
            	$("#detail_even_photo1").html('<img src="/chart_images/' + self._data.event[0].replace(imgsRealPath, "") + '" />');
	       		$("#detail_even_photo2").html('<img src="/chart_images/' + self._data.event[1].replace(imgsRealPath, "") + '" />');
            }
            detailhtmlwidget(self._data.curConn,"#detail_curConn_table","#detail_curConn_photo","#detail_curConn","curConn");
            detailhtmlwidget(self._data.newConn,"#detail_newConn_table","#detail_newConn_photo","#detail_newConn","newConn");
        },
    	reload:function(){
    		$("#outspan").hide();
    		var self = this; 
    		nb.rpc.reportApi.c("getReport",{uid:rUid}).success(function(reportdata){
    			var obj = eval('(' + reportdata + ')');
    			self._data = obj;
    			self._render();
    			$("#outspan").show();
    		});
    	},
    	__init__:function(){
    		var self = this;
            $(self._panel_id).data("nbWidget", this);
            self.reload();         
    	}
    };
   function detailhtmlwidget(data,tableid,photoid,divid,name) {
	    if (data) {
	        if (data[0]) {
	            var table = [];
	            table.push("<table width='85%' class='tabChart' border='0' cellspacing='0' cellpadding='0'><tr><td class='tb01'>设备</td><td  class='tb01'>IP</td><td  class='tb01'>平均利用率%</td></tr>");
	            var datavalue;
	            var classname = "";
	            for (var i = 0; i < data[0].length; i++) {
	            	if(i%2==0){classname="tb02";}
	            	else{classname=="tb03";}
	            	if(name == "availability"){
	            		datavalue = data[0][i].availability?data[0][i].availability:0;
	            	}
	            	else{
	            		datavalue = data[0][i].avgValue;
	            	}
	                table.push("<tr><td  class='"+classname+"'>" + data[0][i].title + "</td><td  class='"+classname+"'>设备IP</td><td  class='"+classname+"'>" + datavalue + "</td></tr>");
	            }
	            table.push("</table>");
	            $(tableid).html(table.join(""));
	        }
	        if (data.length == 2) {
	            $(photoid).html('<img src="/chart_images/' + data[1].replace(imgsRealPath, "") + '" />');
	        }
	    } else {
	        $(divid).hide();
	    }
	}
    
    //===报表配置===
    m.editreportWidget = $.extend({}, editreportBaseWidget, {
        _panel_id: "#editreportWidget",
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
        delReport: function(){
        	if(!confirm("你确定要删除此报表吗？")) return;
            nb.rpc.reportApi.c("delReport", {uid: rUid}).
            success(function(msg){
                nb.AlertTip.storeCookie(msg);
                window.location.href = "/report/index";
            });
        },
        save: function(){
            var self = this;
            var pobj = GetParams(self.viewModel);
            //var params = $.toJSON(pobj);
            
            //params.enable = nb.xutils.val2boolean(params.enable);
            //nb.xutils.delattrs(params, "firstTypes","booleans");
            //params.conditionData.deviceIps = params.conditionData.deviceIps.replace(/\s+/gi, "");
            if(!self._validate(pobj)) return;
            nb.rpc.reportApi.c("editReport", {uid:rUid,medata:pobj}).
            success(function(msg){
                m.fireEvent("alarmRulesChange");
                nb.AlertTip.storeCookie(msg);
            });
        }
    });  
     
    function NewDate(str) { 
    	var date = new Date();
    	str = str.split('/');
		date.setUTCFullYear(str[0], str[1]-1, str[2]); 
        date.setUTCHours(0, 0, 0, 0); 
        return date;
    }
	//===组装数据对象===
	function GetData(RemotData){
		var data = {
			description:RemotData.description,
	        exportFormat:RemotData.exportFormat,
			email:RemotData.toMail.join(";"),
	        timeRange:"0",
	        defaultTime:RemotData.timeRange.defaultTime!=null?RemotData.timeRange.defaultTime:"",
	        filterCondition:{}
		};
		$("#_reportTitle").html(RemotData.description);
		if(RemotData.timeRange.customTime!=null)
		{
			data.timeRange = "1";
			data.startTime =  NewDate(RemotData.timeRange.customTime.startTime);
			data.endTime = NewDate(RemotData.timeRange.customTime.endTime);
			
			$("#_startTime").html(RemotData.timeRange.customTime.startTime+ " 00:00:00");
			$("#_endTime").html(RemotData.timeRange.customTime.endTime+ " 00:00:00");
		}
		else if(RemotData.timeRange.defaultTime!=null){
			var defaulttime = RemotData.timeRange.defaultTime;
			var mydate = new Date();
			var mymonth = mydate.getMonth() + 1;  
			var myday = mydate.getDate();  
		    var lastday = mydate.getDate()-1;
		    var day3 = mydate.getDate()-3;  
		    var myyear = mydate.getFullYear(); 
			if(defaulttime == "day"){
				$("#_startTime").html(myyear+"-"+mymonth+"-"+lastday+" "+mydate.getHours()+":00:00");
				$("#_endTime").html(myyear+"-"+mymonth+"-"+myday+" "+mydate.getHours()+":00:00");
			}
			else if(defaulttime == "3day"){
				$("#_startTime").html(myyear+"-"+mymonth+"-"+day3+" "+mydate.getHours()+":00:00");
				$("#_endTime").html(myyear+"-"+mymonth+"-"+myday+" "+mydate.getHours()+":00:00");			
			}
			else if(defaulttime == "week"){
				var sdate=mydate.getTime()-(1*24*60*60*1000);
                var edate=new Date(sdate-(5*24*60*60*1000));
				$("#_startTime").html(edate.getFullYear()+"-"+(edate.getMonth() + 1)+"-"+edate.getDate()+" "+mydate.getHours()+":00:00");
				$("#_endTime").html(myyear+"-"+mymonth+"-"+myday+" "+mydate.getHours()+":00:00");		
			}
			else if(defaulttime == "month"){
				var sdate=mydate.getTime()-(1*24*60*60*1000);
                var edate=new Date(sdate-(28*24*60*60*1000));
				$("#_startTime").html(edate.getFullYear()+"-"+(edate.getMonth() + 1)+"-"+edate.getDate()+" "+mydate.getHours()+":00:00");
				$("#_endTime").html(myyear+"-"+mymonth+"-"+myday+" "+mydate.getHours()+":00:00");	
			}
			data.startTime ="";
			data.endTime ="";
		}
		data.reportType = [];
		data.reports = [];
		data.objClass_device = [];
		data.objClass_network = [];
		data.objClass_website = [];
		var reporthtml = [];
		if(RemotData.filterCondition.DeviceClass!=null){
			data.reportType.push("DeviceClass");
			if(RemotData.filterCondition.DeviceClass.reports!=null){
				for(var j=0;j<RemotData.filterCondition.DeviceClass.reports.length;j++){
					data.reports.push(RemotData.filterCondition.DeviceClass.reports[j]);
				}
			}
			if(RemotData.filterCondition.DeviceClass.objClass!=null){				
				for(var j=0;j<RemotData.filterCondition.DeviceClass.objClass.length;j++){
					data.objClass_device.push(RemotData.filterCondition.DeviceClass.objClass[j]);
				}
				$("#DeviceClassID").val(data.objClass_device);
			}
		}
		if(RemotData.filterCondition.NetworkClass!=null){
			data.reportType.push("NetworkClass");
			if(RemotData.filterCondition.NetworkClass.reports!=null){				
				for(var j=0;j<RemotData.filterCondition.NetworkClass.reports.length;j++){
					data.reports.push(RemotData.filterCondition.NetworkClass.reports[j]);
				}
			}
			if(RemotData.filterCondition.NetworkClass.objClass!=null){				
				for(var j=0;j<RemotData.filterCondition.NetworkClass.objClass.length;j++){
					data.objClass_network.push(RemotData.filterCondition.NetworkClass.objClass[j]);
				}
				$("#NetworkClassID").val(data.objClass_network);
			}
		}
		if(RemotData.filterCondition.WebSiteClass!=null){
			data.reportType.push("WebSiteClass");
			if(RemotData.filterCondition.WebSiteClass.reports!=null){							
				for(var j=0;j<RemotData.filterCondition.WebSiteClass.reports.length;j++){
					data.reports.push(RemotData.filterCondition.WebSiteClass.reports[j]);
				}
			}
			if(RemotData.filterCondition.WebSiteClass.objClass!=null){
				for(var j=0;j<RemotData.filterCondition.WebSiteClass.objClass.length;j++){
					data.objClass_website.push(RemotData.filterCondition.WebSiteClass.objClass[j]);
				}
				$("#WebSiteClassID").val(data.objClass_website);
			}
		}
		data.reports = uniq(data.reports);
		$("#_reportReports").html(GetReportConent(data.reports).join(" "));
		return data;
	}
	var toObject = function(a) { 
		var o = {}; 
		for (var i=0, j=a.length; i<j; i=i+1) { // 这里我调整了下, YUI源码中是i<a.length 
			o[a[i]] = true; 
		}
		return o; 
	}; 
	var keys = function(o) { 
		var a=[], i; 
		for (i in o) { 
			if (o.hasOwnProperty(i)) { 
				a.push(i); 
			} 
		} 
			return a; 
	}; 
	var uniq = function(a) { 
		return keys(toObject(a)); 
	};
	function GetReportConent(reportlist){
		var html = [];
		for(var i=0;i<reportlist.length;i++){
			if(reportlist[i] == "cpu"){
				html.push("<a href='#acpu'>*Cpu报表</a>");
			}
			else if(reportlist[i] == "mem"){
				html.push("<a href='#amem'>*内存报表</a>");
			}			
			else if(reportlist[i] == "resTime"){
				html.push("<a href='#aresTime'>*响应时间报表</a>");
			}
			else if(reportlist[i] == "availability"){
				html.push("<a href='#aavailability'>*可用性报表</a>");
			}
			else if(reportlist[i] == "event"){
				html.push("<a href='#aevent'>*事件统计报表</a>");
			}
			else if(reportlist[i] == "disk"){
				html.push("<a href='#adisk'>*磁盘报表</a>");
			}
			else if(reportlist[i] == "curConn"){
				html.push("<a href='#acurConn'>*连接数报表</a>");
			}
			else if(reportlist[i] == "newConn"){
				html.push("<a href='#anewConn'>*新建连接数报表</a>");
			}
		}
		return html;
	}
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
				params.timeRange = {customTime:{startTime:kendo.toString(ViewModel.startTime, 'd'),endTime:kendo.toString(ViewModel.endTime, 'd')}};
			}
			for(var j=0;j<ViewModel.reportType.length;j++){
				var obj = $("#"+ViewModel.reportType[j]+"ID");
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
	//===初始化日期控件 ===
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
    //===初始化标签页=== 
	var initTabStrip = function () {
		var original = $("#tabstrip").clone(true);
		original.find(".k-state-active").removeClass("k-state-active");
        $("#tabstrip").kendoTabStrip({ animation: { open: { effects: "fadeIn" } } }).css({ marginRight: "0px" });
		$(".configuration input").change(function() {
			    var tabStrip = $("#tabstrip"),
			        selectedIndex = tabStrip.data("kendoTabStrip").select().index(),
			        clone = original.clone(true);			
			    clone.children("ul")
			         .children("li")
			         .eq(selectedIndex)
			         .addClass("k-state-active")
			         .end();			
			    tabStrip.replaceWith(clone);
			    initTabStrip();
		});
	};
	var outreport = function(){
		var html = $("#reportContentWidget").html();
		//alert(html);
	};
    $(document).ready(function(){   
        initDateUi();
        m.editreportWidget.__init__();
        m.reportContentWidget.__init__();
		initTabStrip();
		outreport();
		
		$(".outreport").click(function(){
			outreport();	
		});
    });
})(jQuery);
