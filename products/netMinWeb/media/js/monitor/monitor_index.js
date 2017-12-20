(function($){
	
	var m = window.monitorIndex = new nb.xutils.Observer();
    var query =  {orgUid:window.orgUid, "orgType":"DeviceClass", locUid:window.locUid};
    
	var widgets=[];

//----------------------------------------------------//	
    hostTree.on("selectOrgNode",function(orgUid, uname, path, locUid){
        window.location.href = "/monitor/deviceCls/"+orgUid + "/" + locUid;
    });
    

    

    var refreshAll = function(){
        $.each(widgets, function(i, widget){
           if($(widget._panel_id).is(":visible")){
               widget.reload();
           } 
        });
        
    };
    
    setInterval(function(){refreshAll()}, 1000*60*2); //2分钟自动刷新所有组件
	
	
//-----------------------------------------------------// 

	
	
	m.deviceListWidget = nb.BaseWidgets.extend("BaseGridListWidget", {
		_panel_id:"#panel_001",
		remoteMethod:"listDevicesBaseInfo",
		remoteView:nb.rpc.monitorViews,
		getRemoteParams: function(){ return query;},
		_columns:[
			{field:"title", title:"名称", template:'<a href="/monitor/device/#=_id#/" name="view_detail"><em class="icon monitor_link"></em> #=title #</a>'},
			{field:"manageIp",title:"IP", width:"110px"},
			{field:"cpu.CPU",title:"Cpu", width:'60px',template:'#=nb.Render.toNum2(cpu.CPU,"%")#'},
			{field:"mem.Mem",title:"Mem", width:'60px', template:'#=nb.Render.toNum2(mem.Mem,"%")#'},
			{field:"status",title:"状态", width:'42px', template:'<span class="status-icon-small #=status#"></span>'},
			{title:"配置", width:'42px', template:'<a href="/monitor/devicesConfigOp/#=_id#/" name="view_detail"> <em class="icon cog_edit"></em> </a>'}
		]
	});

    m.recentlyEventsWidget = nb.BaseWidgets.extend("BaseListWidget", {
		_panel_id:"#panel_002",
		remoteMethod:"getDeviceClsRecentlyEventsBaseInfo",
		remoteView:nb.rpc.monitorViews,
		getRemoteParams: function(){ return query;}
	});
	
	m.devicesAvailabilityImgageWidget = nb.BaseWidgets.extend("BaseAvailabilityImageWidget", {
		_panel_id:"#panel_003",
		chartConf:{legend: {borderWidth:0}},
		remoteMethod:"devicesAvailabilityTopN",
		remoteView:nb.rpc.monitorViews,
		getRemoteParams: function(){
			return $.extend({"timeRange": this.timeRange},query);
		},
		__init__: function(){
		    var self  = this;
			new nb.uiTools.TimeRangeBar(this);
			$(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
		}
	});
	
	m.interfacesAvailabilityImgageWidget = nb.BaseWidgets.extend("BaseAvailabilityImageWidget", {
		_panel_id:"#panel_004",
		
        chartConf: { legend: { 
                                    borderWidth:0,
                                    labelFormatter: function() { return nb.Render.ellipsisStr(this.name, 50); }
        }},

		remoteMethod:"interfacesAvailabilityTopN",
		remoteView:nb.rpc.monitorViews,
		getRemoteParams: function(){
			return $.extend({"timeRange": this.timeRange},query);
		},
		__init__: function(){
		    var self  = this;
			new nb.uiTools.TimeRangeBar(this);
			$(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
		}
	});
	
	m.processesAvailabilityImgageWidget = nb.BaseWidgets.extend("BaseAvailabilityImageWidget", {
		_panel_id:"#panel_005",
		chartConf:{legend: {borderWidth:0}},
		remoteMethod:"processesAvailabilityTopN",
		remoteView:nb.rpc.monitorViews,
		chartConf : {legend: {layout: 'vertical', borderWidth:0}},
		getRemoteParams: function(){
			return $.extend({"timeRange": this.timeRange},query);
		},
		__init__: function(){
		    var self  = this;
			new nb.uiTools.TimeRangeBar(this);
			$(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
		}
	});
	
	m.servicesAvailabilityImgageWidget = nb.BaseWidgets.extend("BaseAvailabilityImageWidget", {
		_panel_id:"#panel_006",
		chartConf:{legend: {borderWidth:0}},
		remoteMethod:"servicesAvailabilityTopN",
		remoteView:nb.rpc.monitorViews,
		getRemoteParams: function(){
			return $.extend({"timeRange": this.timeRange},query);
		},
		__init__: function(){
		    var self  = this;
			new nb.uiTools.TimeRangeBar(this);
			$(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
		}
	});
	

	
//----------------------------------------------------------------//	
    $(document).ready(function(){
        widgets = [
            m.deviceListWidget,
            m.recentlyEventsWidget,
            m.devicesAvailabilityImgageWidget,
            m.interfacesAvailabilityImgageWidget,
            m.processesAvailabilityImgageWidget,
            m.servicesAvailabilityImgageWidget
        ];
        
        $.each(widgets, function(i, widget){ widget.__init__();  });
        
        refreshAll();
		
    }); 

})(jQuery);




