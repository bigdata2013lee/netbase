(function($){
    

    var widgets = [];
    var ipmiWidgets = [];
	var m = window.deviceIndex = new nb.xutils.Observer();
	m.currentDevId = window.moUid;


    m.renderCpus = function(cpu){
      var html = "";
        var space = "&nbsp;&nbsp;";
        
        if("1MinLoad" in cpu){
            cpu["1MinLoad"] = cpu["1MinLoad"] == null ? "N/A" : cpu["1MinLoad"];
            html += "" +"Cpu1分钟负载: " + cpu["1MinLoad"];
        }
        if("5MinLoad" in cpu){
            cpu["5MinLoad"] = cpu["5MinLoad"] == null ? "N/A" : cpu["5MinLoad"];
            html += space + "Cpu5分钟负载: " + cpu["5MinLoad"];
        }
        
        return html;
    };

    m.renderMems = function(mem){
      var html = "";
        var space = "&nbsp;&nbsp;";
        if("AvailMem" in mem){
            $.isNumeric(mem.AvailMem) ? mem.AvailMem*=1024 : "";
            html += "可用内存: " + nb.Render.byte2readable(mem.AvailMem, false, 1024, "N/A");
        }
        if("totalMem" in mem){
            $.isNumeric(mem.totalMem) ? mem.totalMem*=1024 : "";
            html += space + "总内存: " + nb.Render.byte2readable(mem["totalMem"], false, 1024, "N/A");
        }
        if("memBuffer" in mem){
            $.isNumeric(mem.memBuffer) ? mem.memBuffer*=1024 : "";
            html += space + "缓存: " + nb.Render.byte2readable(mem["memBuffer"], false, 1024, "N/A");
        }
        
        if("memAvailReal" in mem){
            $.isNumeric(mem.memAvailReal) ? mem.memAvailReal*=1024 : "";
            html += space + "可用内存: " + nb.Render.byte2readable(mem["memAvailReal"], false, 1024, "N/A");
        }
        return html;
    };
    

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
    
    setInterval(function(){refreshAll()}, 1000*60*3); //3分钟自动刷新所有组件
    
    
    
    
    
	/**
	 * 单线的性能图基类
	 */
	var BaseSinglePerfImgWidget = {
		_data:[],
		_render: function(){
			var self = this;
			var div = $(self._panel_id + " .box:first");
			$(self._panel_id + " .box:first").highcharts('StockChart', {
				rangeSelector : {
					selected : 0, enabled:false,
					buttons: [{type: 'day', count: 1, text: '1d'}, {type: 'all',text: 'All'}]	
				},
				scrollbar:{enabled: false},
				title : {text : self.title},
				
				series : [{
					name :self.serieName,  data : self._data,
					tooltip: { valueDecimals: 2 }
				}]
			});
			

		},
		
		reload: function(){
			var self = this;
			self.remoteView.c(self.remoteMethod, function(){return self.getRemoteParams()}).
			success(function(datas){
				self._data = datas;
				self._render();
			});
			
		},
		__init__:function(){}
	};
	
	
    /**
     * 多线的性能图基类
     */
    var BaseMultiplePerfImgWidget = {
        _data:[],
        afterRemote:function(datas){},
        _legendRight:true,
        _render: function(){
            var self = this;
            var legend ={
                    enabled:true, showInLegend:true, borderWidth:0
            };
            
            if(self._legendRight){
                $.extend(legend,{layout:'vertical', align:'right', verticalAlign:'top', x:-1, y:100});
            }

            var div = $(self._panel_id + " .box:first");
            $(self._panel_id + " .box:first").highcharts('StockChart', {
                rangeSelector : {
                    selected : 0, enabled:false,
                    buttons: [{type: 'day', count: 1, text: '1d'}, {type: 'all',text: 'All'}]   
                },
                scrollbar:{enabled: false},
                title : {text : self.title},
                legend:legend,
                series :  self.series
            });
            

        },
        
        reload: function(){
            var self = this;
            if(self.ableReload === false) return;
            nb.uiTools.panelLoading.insertTo(self._panel_id);
            self.remoteView.c(self.remoteMethod, function(){return self.getRemoteParams()}).
            success(function(datas){
                nb.uiTools.panelLoading.cancel(self._panel_id);
                self.afterRemote(datas);
                self.series = datas;
                self._render();
            });
            
        },
        __init__:function(){}
    };
    
    m.baseInfoWidget = nb.BaseWidgets.extend("baseInfoWidget", {
        _panel_id: "#dev_panel_001",
        remoteView:nb.rpc.deviceViews,
        remoteMethod:"getDeviceBaseInfo",
        getRemoteParams:function(){return {"uid": m.currentDevId}},
        
        
        
        onLoad:function(){
            var self = this;
            nb.Render.createCpuMemGauge(self._data.cpu.CPU,self._data.mem.Mem);
            
            var gkSpan = $(self._panel_id + " span.cpu_gk_span");
            if(/^\s*$/.test(gkSpan.text())){ //无内容
                gkSpan.parent().hide();
            }
            
        }
    });
    
    
    m.raidInfoWidget = nb.BaseWidgets.extend("baseInfoWidget", {
        _panel_id: "#raidInfoWidget",
        remoteView:nb.rpc.monitorViews,
        remoteMethod:"getRaidInfos",
        getRemoteParams:function(){return {moUid: m.currentDevId, moType:"Device"}},
        
        onLoad:function(){
            var self = this;
        }
    });
    
    m.tempAndFanInfoWidget = nb.BaseWidgets.extend("baseInfoWidget", {
        _panel_id: "#tempAndFanInfoWidget",
        remoteView:nb.rpc.monitorViews,
        remoteMethod:"getTempAndFanInfos",
        getRemoteParams:function(){return {moUid: m.currentDevId, moType:"Device"}},
        
        onLoad:function(){
            var self = this;
        }
    });
    
	
    m.recentlyEventsWidget = nb.BaseWidgets.extend("BaseListWidget", {
		_panel_id:"#dev_panel_002",
		remoteMethod:"getDeviceClsRecentlyEventsBaseInfo",
		remoteView:nb.rpc.deviceViews,
		getRemoteParams: function(){ return {uid: m.currentDevId};},
        __init__: function(){
            var self = this;
            $(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
        }
	});
	
	m.interfacesListWidget = nb.BaseWidgets.extend("BaseListWidget", {
		_panel_id:"#dev_panel_004",
		remoteMethod:"getDevInterfaces",
		remoteView:nb.rpc.deviceViews,
		getRemoteParams: function(){ return {uid: m.currentDevId};},
        __init__: function(){
            var self = this;
            $(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
        }
	});
	
	
	m.fileSystemsListWidget = nb.BaseWidgets.extend("BaseListWidget", {
		_panel_id:"#dev_panel_005",
		remoteMethod:"getDevFileSystems",
		remoteView:nb.rpc.deviceViews,
		getRemoteParams: function(){ return {uid: m.currentDevId};},
        __init__: function(){
            var self = this;
            $(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
        }
	});
	
	m.processesListWidget = nb.BaseWidgets.extend("BaseListWidget", {
		_panel_id:"#dev_panel_006",
		remoteMethod:"getDevProcesses",
		remoteView:nb.rpc.deviceViews,
		getRemoteParams: function(){ return {uid: m.currentDevId};},
        __init__: function(){
            var self = this;
            $(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
        }
	});
	
	m.ipServicesListWidget = nb.BaseWidgets.extend("BaseListWidget", {
		_panel_id:"#dev_panel_007",
		remoteMethod:"getDevIpServices",
		remoteView:nb.rpc.deviceViews,
		getRemoteParams: function(){ return {uid: m.currentDevId};},
        __init__: function(){
            var self = this;
            $(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
        }
	});
	
	
    m.cpuMemPerfImgWidget = $.extend({},BaseMultiplePerfImgWidget,{
        title:" ",
        timeUnit:"day",
        _panel_id:"#cpuMemPerfImgWidget",
        remoteView:nb.rpc.deviceViews,
        remoteMethod:"getDeviceCpuMemPerfs",
        getRemoteParams: function(){
            var self = this;
            return {uid: m.currentDevId, timeUnit:self.timeUnit};
        },
        
        afterRemote: function(datas){
            $.each(datas, function(i, item){
                item.tooltip={ valueDecimals: 2,valueSuffix:'%' };
            });
        },
        __init__: function(){
            var self = this;
            new nb.uiTools.TimeUnitBar(self);
            $(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
        }
    });


    m.ipInterfacesPerfImgWidget = nb.BaseWidgets.extend("multiPerfImgWidget",{
        _panel_id:"#ipInterfacesPerfImgWidget",
        _currentMoUids:[],
        _max:2,
        cookieName:"iface_perf_currentMoUids",
        remoteView:nb.rpc.deviceViews,
        perfsRemoteMethod:"getInterfacePerfs", //读取对象性能图数据的方法
        getPerfsRemoteMethodParams: function(moUid){
            var self = this;
            return {uid:moUid, timeUnit:self.timeUnit};
        },
        moListRemoteMethod:"getDevInterfaces", //读取对象列表的方法
        getMoListRemoteMethodParams: function(){
            var self = this;
            return {uid:m.currentDevId, simple:true};
        }

    });
    


    m.processesPerfImgWidget = nb.BaseWidgets.extend("multiPerfImgWidget",{
        _panel_id:"#processesPerfImgWidget",
        _currentMoUids:[],
        _max:2,
        cookieName:"process_perf_currentMoUids",
        remoteView:nb.rpc.deviceViews,
        perfsRemoteMethod:"getProcessPerfs", //读取对象性能图数据的方法
		_stockChartConf:function(item){
			return {
				rangeSelector : { selected : 0, enabled:false},
				scrollbar:{enabled: false},
				title : {text : nb.Render.ellipsisStr(item.title, 34), style:{fontSize: '12px', color:"#730000"}},
				//legend:legend,
				tooltip:{
				    formatter:function(tooltip){
				        var items = this.points || splat(this);
				        var series = items[0].series; var s=[];
				
				        // build the header
				        s = [series.tooltipHeaderFormatter(items[0])];
				
				        // build the values
				        $.each(items, function (i,item) {
				            var point = item.point;
				            series = item.series;
				               var pointFormat = '<span style="color:{0}">{1}</span>: <b>{2}</b><br/>';
				               var x="";
				               if(series.name == "Cpu"){
				                   x = nb.xutils.formatStr(pointFormat, series.color, series.name, nb.Render.toNum2(point.y, '%'));
				               }
				               else if(series.name == "Mem"){
				                   x = nb.xutils.formatStr(pointFormat, series.color, series.name, nb.Render.byte2readable(point.y, false, 1000));
				               }
				               s.push(x);
				        });
				
				        // footer
				        s.push(tooltip.options.footerFormat || '');
				
				        return s.join('');
				    }
				},
				yAxis: [{
				    title: {text: 'Mem' },
				    height: 120, lineWidth: 1
				}, {
				    title: { text: 'Cpu' },
				    top: 150, offset: 0,
				    height: 120, lineWidth: 1
				}],
				series :  item.series
			}
		},
        getPerfsRemoteMethodParams: function(moUid){
            var self = this;
            return {uid:moUid, timeUnit:self.timeUnit};
        },
        moListRemoteMethod:"getDevProcesses", //读取对象列表的方法
        getMoListRemoteMethodParams: function(){
            var self = this;
            return {uid:m.currentDevId, simple:true};
        }
    });
    


    $(document).ready(function() {
    	widgets=[
            m.baseInfoWidget,
            m.raidInfoWidget,
            m.tempAndFanInfoWidget,
            m.recentlyEventsWidget,
            m.interfacesListWidget,
            m.processesListWidget,
            m.fileSystemsListWidget,
            m.ipServicesListWidget,
            m.cpuMemPerfImgWidget,
            m.ipInterfacesPerfImgWidget,
            m.processesPerfImgWidget
    	];
    	
    	ipmiWidgets = []
    	
    	$.each(widgets, function(i, widget){
    	    widget.__init__();
    	});
    	
    	
    	refreshAll();
    	
    	
    });
	
	
})(jQuery);








