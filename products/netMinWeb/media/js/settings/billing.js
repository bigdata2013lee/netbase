(function($) {
	var m = new nb.xutils.Observer();
	
	m.addBillingWidget = {
		_types:["Device","Network","Website","Bootpo","ShortcutCmd"],
		_panel_id:"#addBillingWidget",
		unitPrices:{},
		_countTotalPrice:function(){
			var  self = this;
			var total = 0;
			var counts = self.getCounts();
			$.each(self._types, function(i,name){
				total += (counts[name] || 0) * (self.unitPrices[name] || 0);
			})
			var months = $(self._panel_id + " select[name=months]").val() * 1;
			return total * months;
		},
		getCounts:function(){
			var  self = this;
			var counts = {};
			$.each(self._types, function(i,name){
				var numBox = $(self._panel_id + " input.number[name="+name+"]").data("kendoNumericTextBox");
				counts[name] = numBox ? numBox.value() : 0;
			})
			return  counts;
		},
		_loadUnitPrices:function(){
			var  self = this;
			self.unitPrices = {Device: 20, Website:10, Bootpo:50, ShortcutCmd:5, Network:20};
		},
		
		_setTotalPrice:function(price){
			var  self = this;
			$(self._panel_id + " span[name=totalPrice]").text(price + " 元");
		},
		
		checkCount: function(counts){
			var flag = false;
			$.each(counts, function(k, v){
				if(v != 0){
					flag = true;
				}
			});
			
			return flag;
		},
		
		save:function(){
			var  self = this;
			var counts = self.getCounts();
			var months = $(self._panel_id + " select[name=months]").val() * 1;
			var params = {counts:counts, months:months};
			nb.rpc.billingViews.c("addBilling", params).success(function(msg){
				var _type = "confirmation";
				if(/^\s*\w*_*warn\:(.+)/gi.test(msg)){
					msg = RegExp.$1;
					_type = "error";
				}
				
				if(_type == "error"){
					msg += '<br/><br/><a class="try-kendo">充值导购指引&gt;&gt;</a>';
				}
				
		    	var dialog = new $.Zebra_Dialog(msg, {
				    'modal': true, 'width':500,
				    overlay_opacity:0.1,
				    overlay_close:false,
				    type:_type,
				    buttons:[]
				});
			})
		},
		__init__ : function(){
			var  self = this;
			self._loadUnitPrices();
			$(self._panel_id + " input.number").kendoNumericTextBox({
			 	format: "#",
			 	spin:function(){
			 		var tp = self._countTotalPrice();
			 		self._setTotalPrice(tp);
			 	},
			 	change:function(){
					var tp = self._countTotalPrice();
			 		self._setTotalPrice(tp);
			 	}
			 });
			 
			 $(self._panel_id + " select[name=months]").bind("change",function(){
				var tp = self._countTotalPrice();
			 	self._setTotalPrice(tp);
			 })
			 
			 $(self._panel_id + " button[name=save]").bind("click", function(){
				var counts = self.getCounts();
				if(! self.checkCount(counts)){
					alert("购买个数不能全为空");
					return;
				}
			 	if(!window.confirm("您已经仔细核对购买项目，并确定购买？")){return}
			 	self.save();
			 });
			 var totalPrice = self._countTotalPrice();
			 self._setTotalPrice(totalPrice);
			
			
		}
		
		
	}
	
	
	
    m.listBillingsWidget =  nb.BaseWidgets.extend("BaseListWidget", {
		_panel_id:"#listBillingsWidget",
		__pageSize:8,
		remoteMethod:"listBillings",
		remoteView:nb.rpc.billingViews,
		getRemoteParams: function(){var self=this; return {};},
		__init__: function(){
            var self = this;
            self.reload();
            $(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
        }
	});
	
	
	

	m.sourcesUsedCaseChartWidget = {
		chartConf : {},
		_panel_id:"#sourceChart",
		remoteView:nb.rpc.billingViews,
		remoteMethod:"getChartData",
		_render: function(data){
			var self =this;
			var series = data.series;
			var categories = data.categories;
			var _charts = {
				title: {text: '图表统计未来30天项目变化'},
				xAxis: { categories: categories, labels:{rotation:30}},
				yAxis: {
					title: {text: '个数'},min:0,
					plotLines: [{value: 0, width: 1, color: '#808080'}]
				},
				legend: {
					layout: 'vertical', align: 'right', 
					verticalAlign: 'middle', borderWidth:0

				},
				series: series
			};
			_charts = $.extend(_charts, self.chartConf)
			$(self._panel_id + ' div.box:first').highcharts(_charts);
		},
		reload:function(){
			var self = this;
			nb.uiTools.panelLoading.insertTo(self._panel_id);
			var params = self.getRemoteParams ? self.getRemoteParams() : {};
			self.remoteView.c(self.remoteMethod,params)
			.success(function(data){
			    nb.uiTools.panelLoading.cancel(self._panel_id);
				self._render(data);
			});

		},
		__init__:function(){
			var self = this;
			$("#user_left_menus a[name=sourcesUsedCase]").one("click",function(){
				self.reload();
			})
		}
	};


	m.sourcesUsedCaseTableWidget = {
		_panel_id:"#sourcesUsedCaseTableWidget",
		_render:function(counts){
			var self = this;
			$.each(counts, function(name, count){
				$(self._panel_id + " span.count[name="+name+"]").text(count)
			})
		},
		
		reload:function(){
			var self = this;
			var data = {Device:21, Network:1};
			nb.rpc.billingViews.c("getCurrentSourcesUsedCounts").
			success(function(counts){
				self._render(counts);
			})
		},
		
		__init__:function(){
			var self = this;
			self.reload();
		}
	}
	
    $(document).ready(function(){
    	m.addBillingWidget.__init__();
    	m.listBillingsWidget.__init__();
    	m.sourcesUsedCaseChartWidget.__init__();
    	m.sourcesUsedCaseTableWidget.__init__();
    })

})(jQuery);