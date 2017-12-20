(function($){
	
	var m = window.websiteIndex = new nb.xutils.Observer();
	m.current = {};
	m.current.websiteClsUid = window.orgUid;
    var widgets = [];
    
    websuteClsTree.on("selectOrgNode", function(orgUid, uname){
        window.location.href = "/website/websiteCls/" + orgUid
    });
    
    var refreshAll = function(){
        $.each(widgets, function(i, widget){
           if($(widget._panel_id).is(":visible")){
               widget.reload();
           } 
        });
        
    };
    	

	var TimeRangeBar = nb.Class({
		__init__: function(widget){
			var el = $(widget._panel_id + " div.timeRangeBar");
			this.widget = widget; 
			var self = this;
			
			$(el).find(">span").bind("click", function(){
				if($(this).is(".selected")) return;
				$(this).siblings().removeClass("selected");
				$(this).addClass("selected");
				var val = $(this).attr("value") * 1;
				self.setRange(val);
			});
		},
		

		setRange: function(r){
			this.widget.timeRange = r;
			this.widget.reload();
		}
	});
	var createDs = function(data){
		
		var inline = new kendo.data.HierarchicalDataSource({
			data:data
		});
		
		return inline;
	};
	

	
    m.recentlyEventsWidget = nb.BaseWidgets.extend("BaseListWidget", {
        _panel_id:"#panel_0002",
        remoteMethod:"getWebsiteClsRecentlyEvents",
        remoteView:nb.rpc.websiteViews,
        getRemoteParams: function(){return {"websiteClsUid":m.current.websiteClsUid}}
    });
	
	m.listAvailabilityWidget = nb.BaseWidgets.extend("BaseListWidget", {
		_panel_id: "#panel_0001",
		remoteMethod:"listAvailability",
        remoteView:nb.rpc.websiteViews,
        getRemoteParams: function(){return {"websiteClsUid":m.current.websiteClsUid}},
        afterInit: function(){
            var self = this;
            $(self._panel_id + " tbody:first").delegate(">tr:not(.nested_tr)", "click", function(evt){
               $(this).next(".nested_tr").fadeToggle();
            });
        }
	});


	m.listAvgAndCurReponseWidget = nb.BaseWidgets.extend("BaseListWidget", {
		_panel_id: "#panel_0005",
		remoteMethod:"listWebSiteReponseTime",
        remoteView:nb.rpc.websiteViews,
        getRemoteParams: function(){return {"websiteClsUid":m.current.websiteClsUid}},
        afterInit: function(){
            var self = this;
            $(self._panel_id + " tbody:first").delegate(">tr:not(.nested_tr)", "click", function(evt){
               $(this).next(".nested_tr").fadeToggle();
            });
        }
	});
//------------------------------------------------//	
$(document).ready(function(){
		
	m.availabilityImageWidget = {
		timeRange: 3600,
		_panel_id: "#panel_0003",
		_render: function(data){
			var series = data.series;
			var categories = data.categories;
			$.each(series, function(i, item){
				$.each(item.data, function(j, val){
					val = nb.Render.percent(val);
					item.data[j] = val;
				});
			});
			$(this._panel_id + ' div.box:first').highcharts({
				title: { text: ' ' },

				xAxis: { categories: categories, labels:{rotation:30}},
				yAxis: {
					title: {text: '可用性 (%)' },
					plotLines: [{
						value: 0, width: 1, color: '#808080'
					}]
				},
				tooltip: { valueSuffix: '%' },
				legend: {
					//layout: 'vertical', align: 'right', verticalAlign: 'middle',  
					borderWidth: 0
				},
				series: series
			});
		},
		reload:function(){
			var self = this; 
            nb.uiTools.panelLoading.insertTo(self._panel_id);
            nb.rpc.websiteViews.c("getAvailabilityData",{websiteClsUid:m.current.websiteClsUid, timeRange: this.timeRange})
            .success(function(data){
                nb.uiTools.panelLoading.cancel(self._panel_id);
				self._render(data);
            });

		},
        __init__: function(){
            var self  = this;
            new TimeRangeBar(self);
            $(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
        }
	};

	m.responesTimeTopsWidget = {
		timeRange: 3600,
		_panel_id: "#panel_0004",
		_render: function(data){
			var series = data.series;
			var categories = data.categories;
			$.each(series, function(i, item){
				$.each(item.data, function(j, val){
					val = nb.Render.toNum2(val);
					item.data[j] = val;
				});
			});
			$(this._panel_id + ' div.box:first').highcharts({
				title: { text: ' ' },

				xAxis: { categories: categories, labels:{rotation:30}},
				yAxis: {
					title: { text: 'time (sec)' },
					plotLines: [{
						value: 0, width: 1, color: '#808080'
					}]
				},
				tooltip: { valueSuffix: 's' },
				legend: {
					//layout: 'vertical', align: 'right', verticalAlign: 'middle',  
					borderWidth: 0
				},
				series: series
			});
		},
		reload:function(){
			var self = this; 
			nb.uiTools.panelLoading.insertTo(self._panel_id);
            nb.rpc.websiteViews.c("getResponesTimeTopsData",{websiteClsUid:m.current.websiteClsUid, timeRange: this.timeRange})
            .success(function(data){
                nb.uiTools.panelLoading.cancel(self._panel_id);
				self._render(data);
            });

		},
        __init__: function(){
            var self  = this;
            new TimeRangeBar(self);
            $(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
        }		
	};

    
    /**
     *摘要组件 
     */
    m.summaryWidget = {
        _panel_id:"#summaryWidget",
        _data:{},
        _render: function(){
            var self = this;
            var template = self.getTemplate();
            $(self._panel_id + " .box:first").html(template(self._data));  
        },
        getTemplate: function(){
            var template = kendo.template($(this._panel_id + " script[name=template]").html());
            return template;
        },
        _countInfo: function(){
            var self = this;
            var info = self._data;
            info.avgScore = info.scores / (info.allMosCount || 1);
            info.avgScore = window.parseInt(info.avgScore, 10);
            if(info.avgScore>=70){ info.status = "良好"; info.statusColor="#14A006"; }
            else if(info.avgScore>=40){ info.status = "一般"; info.statusColor="#1279BC"; }
            else if(info.avgScore<=40){ info.status = "比较差"; info.statusColor="#D90000"; }
            else{ info.status = "未知"  }
            
        },
        reload:function(){
            var self = this;
            nb.rpc.websiteViews.c("getSummaryInfo")
            .success(function(info){
                self._data = info;
                self._countInfo();
                self._render();
            });
        
        },
        __init__:function(){
          var self = this;
          self.reload();
        }
    
    };


	
}); //end ready.
//------------------------------------------------//
$(document).ready(function(){
	
	m.summaryWidget.__init__();
	m.summaryWidget.reload();
	widgets = [
    	m.listAvailabilityWidget,
    	m.recentlyEventsWidget,
    	m.listAvgAndCurReponseWidget,
    	m.availabilityImageWidget,
        m.responesTimeTopsWidget
	]
    
    $.each(widgets, function(i, widget){
        widget.__init__();
    });
    
    refreshAll();
	
});
	
	
})(jQuery);
