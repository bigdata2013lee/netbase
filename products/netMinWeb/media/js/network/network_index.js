(function($){
	
	var m = window.networkIndex = new nb.xutils.Observer();
    var query =  {orgUid:window.orgUid, "orgType":"NetworkClass"};
    m.currentNetUid = null;
	var widgets = [];
//----------------------------------------------------//	
    networkTree.on("selectOrgNode",function(orgUid, uname){
        window.location.href = "/network/networkCls/"+orgUid;
    });
    
    networkTree.on("selectMoNode", function(netId){
        window.location.href = "/network/network/"+netId;
    });

	
//-----------------------------------------------------// 

	m.networkListWidget = nb.BaseWidgets.extend("BaseListWidget", {
		_panel_id:"#panel_001",
		remoteMethod:"listNetworks",
		remoteView:nb.rpc.networkViews,
		getRemoteParams: function(){ return query;}
	});

    m.recentlyEventsWidget = nb.BaseWidgets.extend("BaseListWidget", {
		_panel_id:"#panel_002",
		remoteMethod:"getOrgRecentlyEvents",
		remoteView:nb.rpc.networkViews,
		getRemoteParams: function(){ return query;}
	});
	
	m.networksAvailabilityImgageWidget = nb.BaseWidgets.extend("BaseAvailabilityImageWidget", {
		_panel_id:"#panel_003",
		chartConf:{legend: {borderWidth:0}},
		remoteMethod:"networksAvailabilityTopN",
		remoteView:nb.rpc.networkViews,
		getRemoteParams: function(){
			return $.extend({"timeRange": this.timeRange},query);
		},
		__init__: function(){
		    var self = this;
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
        remoteView:nb.rpc.networkViews,
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
    $(document).ready(function() {
    	
    	widgets=[m.networkListWidget,m.networksAvailabilityImgageWidget,
    	m.recentlyEventsWidget,m.interfacesAvailabilityImgageWidget ];
    	
        $.each(widgets, function(i,widget){
        	widget.__init__();
        	widget.reload();
        })
		
    }); 
})(jQuery);




