(function($){
	var m = window.networkIndex = new nb.xutils.Observer();
	m.currentNetId = window.moUid;
	   window.testPointy = function(y){
        return y + "bps."
    }
    var cookieName = "interfaceIds";
    m.interfacesIdShowAtPage = [];
    m.cookieVal = [];
	//----------------------------------------------------//	
    networkTree.on("selectOrgNode",function(orgUid, uname){
        window.location.href = "/network/networkCls/"+orgUid;
    });
    
    networkTree.on("selectMoNode", function(netId){
        window.location.href = "/network/network/"+netId;
    });
        
    var add2Cookie = function(val, cookieValx){
    	cookieValx.push(val);
    	m.cookieVal = cookieValx;
    	$.cookie(cookieName, $.toJSON(cookieValx), {expires:7});
    };
    
    var del2Cookie = function(val, cookieValx){
    	cookieValx.splice($.inArray(val,cookieValx),1);
    	m.cookieVal = cookieValx;
    	$.cookie(cookieName, $.toJSON(cookieValx), {expires:7});
    };
    

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
            html += "可用内存: " + nb.Render.byte2readable(mem.AvailMem/1024, false, 1024, "N/A");
        }
        if("totalMem" in mem){
            $.isNumeric(mem.totalMem) ? mem.totalMem*=1024 : "";
            html += space + "总内存: " + nb.Render.byte2readable(mem["totalMem"]/1024, false, 1024, "N/A");
        }
        if("memBuffer" in mem){
            $.isNumeric(mem.memBuffer) ? mem.memBuffer*=1024 : "";
            html += space + "缓存: " + nb.Render.byte2readable(mem["memBuffer"]/1024, false, 1024, "N/A");
        }
        
        if("memAvailReal" in mem && mem["memAvailReal"]){
            $.isNumeric(mem.memAvailReal) ? mem.memAvailReal*=1024 : "";
            html += space + "可用内存: " + nb.Render.byte2readable(mem["memAvailReal"]/1024, false, 1024, "N/A");
        }
        return html;
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
            nb.uiTools.panelLoading.insertTo(self._panel_id);
            self.remoteView.c(self.remoteMethod, function(){return self.getRemoteParams()}).
            success(function(datas){
                nb.uiTools.panelLoading.cancel(self._panel_id);
                self.afterRemote(datas);
                self.series = datas;
                self._render();
            });
            
        }
    };
	
	
    m.baseInfoWidget = nb.BaseWidgets.extend("baseInfoWidget", {
        _panel_id: "#dev_panel_001",
        remoteView:nb.rpc.networkViews,
        remoteMethod:"getBaseInfo",
        getRemoteParams:function(){return {"uid": m.currentNetId}},
        
        
        
        onLoad:function(){
            var self = this;
            nb.Render.createCpuMemGauge(self._data.cpu.CPU,self._data.mem.Mem);
            
            var gkSpan = $(self._panel_id + " span.cpu_gk_span");
            if(/^\s*$/.test(gkSpan.text())){ //无内容
                gkSpan.parent().hide();
            }
            
        }
    });
    
    m.recentlyEventsWidget = nb.BaseWidgets.extend("BaseListWidget", {
        _panel_id:"#dev_panel_002",
        remoteMethod:"getNetworkClsRecentlyEvents",
        remoteView:nb.rpc.networkViews,
        getRemoteParams: function(){ return {uid: m.currentNetId};},
        __init__: function(){
            var self = this;
            $(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
        }
    });

	m.interfacesListWidget = nb.BaseWidgets.extend("BaseGridListWidget", {
        _panel_id:"#interfacesListWidget",
        _gridConf:{height:300},
        remoteMethod:"getNetworkInterfaces",
        remoteView:nb.rpc.networkViews,
        getRemoteParams: function(){return {uid:m.currentNetId}},
        _columns: [
        	{field : "uname", title : "名称", width : 60},
        	{field : "ipAddress", title : "IP地址", width : 90},
        	{field : "throughValues.input", title : "流入", width : 60, template:"#=nb.Render.byte2readable(throughValues.input, true)#"},
        	{field : "throughValues.output", title : "流出", width : 60, template:'#=nb.Render.byte2readable(throughValues.output,true)#' },
        	{field : "status", title : "状态", width : 40, template:'<span class="status-icon-small  #=status#"></span>'},
        	{field : "", title : "性能图", width : 40, template:' \
	<input type="checkbox" class="formID" formid="#=_id#" \
	#if(networkIndex.cookieVal.indexOf(_id) != -1){#	\
		checked \
	#}# />'}        
        ],
        
        afterInit: function(){
        	var self = this;
        	var selectInCookie = [];
        	if( ! $.isEmptyObject($.cookie(cookieName))){
        		selectInCookie = $.evalJSON($.cookie(cookieName));
        	}
       		m.cookieVal = selectInCookie;       		
        	$(self._panel_id + " div.data_grid").delegate("input.formID", "click", function(){
        		var _id = $(this).attr("formid");
        		if(selectInCookie.length == 10 && $(this).prop("checked")){
        			$(this).prop("checked", "");
        			alert("最多选择10个");
        			return;
        		}
        		if($(this).prop("checked")){
        			
        			if($.inArray(_id, selectInCookie) == -1){
						add2Cookie(_id, selectInCookie);
        				m.ipInterfacesPerfImgWidget.hasSelectInterface = m.cookieVal;
        				m.ipInterfacesPerfImgWidget.reload();
        			}
        		}else{
        			if($.inArray(_id, selectInCookie) != -1){
        				del2Cookie(_id, selectInCookie);
        				m.ipInterfacesPerfImgWidget.hasSelectInterface = m.cookieVal;
        				m.ipInterfacesPerfImgWidget.reload();
        			}       			
        		}
        	});
        }
        
    });
    
    
	 m.firewallConnImageWidget = $.extend({},BaseMultiplePerfImgWidget,{
        title:" ",
        timeUnit:"day",
        _panel_id:"#firewallConnImageWidget",
        remoteView:nb.rpc.networkViews,
        remoteMethod:"getNetworkFireWallPerfs",
        getRemoteParams: function(){
            var self = this;
            return {uid: m.currentNetId, timeUnit:self.timeUnit};
        },
        
        afterRemote: function(datas){
            $.each(datas, function(i, item){
                item.tooltip={ valueDecimals: 1};
            });
        },
        __init__: function(){
            var self = this;
            new nb.uiTools.TimeUnitBar(self);
            $(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
        }
    });   
	
	
	 m.cpuMemPerfImgWidget = $.extend({},BaseMultiplePerfImgWidget,{
        title:" ",
        timeUnit:"day",
        _panel_id:"#cpuMemPerfImgWidget",
        remoteView:nb.rpc.networkViews,
        remoteMethod:"getNetworkCpuMemPerfs",
        getRemoteParams: function(){
            var self = this;
            return {uid: m.currentNetId, timeUnit:self.timeUnit};
        },
        
        afterRemote: function(datas){
            $.each(datas, function(i, item){
                item.tooltip={ valueDecimals: 1,valueSuffix:'%' };
            });
        },
        __init__: function(){
            var self = this;
            new nb.uiTools.TimeUnitBar(self);
            $(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
        }
    });
    
    
     m.ipInterfacesPerfImgWidget = $.extend({},{
        _panel_id:"#ipInterfacesPerfImgWidget",
        timeUnit:"day",
        remoteView:nb.rpc.networkViews,
        remoteMethod:"getInterfacesPerfs",
        hasSelectInterface: [],
        getRemoteParams: function(){
            var self = this;
            return {uid: m.currentNetId, timeUnit:self.timeUnit, hasSelectInterface: self.hasSelectInterface};
        },
        afterRemote:function(datas){
            
        },
        _legendRight:true,
        _render: function(){
            var self = this;
            var legend ={
                    enabled:true, showInLegend:true, borderWidth:0
            };
            
            if(self._legendRight){
                $.extend(legend,{layout:'vertical', align:'right', verticalAlign:'top', x:-1, y:100});
            }
            var boxDiv = $(self._panel_id + " div.box:first").html("");
            $.each(self.datas, function(i, item){
                var div = $("<div class='chart_div'></div>");
                div.appendTo(boxDiv);
                div.highcharts('StockChart', {
                    rangeSelector : { selected : 0, enabled:false},
                    scrollbar:{enabled: false},
                    title : {text : nb.Render.ellipsisStr(item.title, 34), style:{fontSize: '12px', color:"#730000"}},
                    legend:legend,
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
                                   var x = nb.xutils.formatStr(pointFormat, series.color, series.name, nb.Render.byte2readable(point.y, true));
                                   s.push(x);
                            });
                    
                            // footer
                            s.push(tooltip.options.footerFormat || '');
                    
                            return s.join('');
                        }
                    },
                    
                    series :  item.series
                });
                
            });
            boxDiv.append("<br clear='both' />");
            
            

        },
        
        reload: function(){
            var self = this;
            nb.uiTools.panelLoading.insertTo(self._panel_id);
            self.remoteView.c(self.remoteMethod, function(){return self.getRemoteParams()}).
            success(function(datas){
                nb.uiTools.panelLoading.cancel(self._panel_id);
                self.afterRemote(datas);
                self.datas = datas;
                self._render();
            });
            
        },
        __init__: function(){
            var self = this;
            self.hasSelectInterface = m.cookieVal;
            new nb.uiTools.TimeUnitBar(self);
            $(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
        }
    });
    
    
   //-----------------------------END MultSelect--------------------------------------------------------------------------------- 
    
    $(document).ready(function() {
    	widgets = [m.baseInfoWidget, m.recentlyEventsWidget, m.interfacesListWidget, m.ipInterfacesPerfImgWidget,
    	m.cpuMemPerfImgWidget];
    	if(networkType=="firewall"){
    		m.firewallConnImageWidget.__init__();
    		m.firewallConnImageWidget.reload();
    	}
    	$.each(widgets, function(i,widget){
    		widget.__init__();
    		widget.reload();
    	});
    	
        //m.ipInterfacesPerfImgWidget.__init__();
        //m.ipInterfacesPerfImgWidget.reload();
        //$.cookie(cookieName, $.toJSON([]), {expires:3, path:"/"});
       
    });
	
	
})(jQuery);








