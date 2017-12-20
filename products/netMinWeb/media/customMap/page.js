(function($){
	
	
	var ns = nb.nameSpace("customerMapPage");
	var m = new nb.xutils.Observer();
	
	
	var pageReload=function(){
		window.location.reload();
	}
	m.customerMapListWidget = nb.BaseWidgets.extend("BaseListWidget", {
		_panel_id:"#customerMapListWidget",
		__body:"ul:first",
		remoteMethod:"listCustomerMaps",
		remoteView:nb.rpc.customerMapViews,
		getRemoteParams: function(){ return {};},
		onLoad:function(){
			var self = this;
			setTimeout(function(){
				$(self._panel_id + " a[name=view_customer_map]:first").click();
			}, 1000*0.5)
		}
	});
	
	
	
	m.addCustomermapWidget = {
		_panel_id:"#addCustomerMapWidget",
		_validate:function(params){
			var self = this;
			var em = $(self._panel_id + " div.validateErrorMsg");
            var messages = {title:"标题为必填项，请重新输入(中文\数字\字母\_ 2~10个字符)", zIndex:"排列序号应该填写小于4位的数字"};
            var rules = {title: {method:"regex", exp:/^[0-9a-zA-Z_\u4e00-\u9fa5]{2,10}$/},zIndex: {method:"regex", exp:/^\s*\d{1,4}\s*$/}};
            var validator = new nb.xutils.Validator(em, rules, messages);
            return validator.validate(params);
		},
		save:function(){
			var self = this;
			var params = nb.uiTools.mapFields(self._panel_id + " div.box");
			if(!self._validate(params)){return;}
			params.zIndex*=1;
			nb.uiTools.closeEditDialogWin(self._panel_id);
			nb.rpc.customerMapViews.c("createCustomerMap", params).success(function(msg){
				nb.AlertTip.storeCookie(msg);
				pageReload();
			})
		},
		__init__:function(){
			var self = this;
			$("a[name=add_customer_map]").bind("click", function(){
				nb.uiTools.showEditDialogWin(null, self._panel_id, {title:"添加\创建自定义拓朴图", width:500, height:200});
			});
			
			$(self._panel_id + " button.ok").bind("click", function(){
				self.save();
			})
		}
	}
	
	
	
	m.editCustomerMapPropsWidget = {
		_panel_id:"#editCustomerMapPropsWidget",
		_validate:function(params){
			var self = this;
			var em = $(self._panel_id + " div.validateErrorMsg");
            var messages = {title:"标题为必填项，请重新输入(中文\数字\字母\_ 2~10个字符)", zIndex:"排列序号应该填写小于4位的数字"};
            var rules = {title: {method:"regex", exp:/^[0-9a-zA-Z_\u4e00-\u9fa5]{2,10}$/},zIndex: {method:"regex", exp:/^\s*\d{1,4}\s*$/}};
            var validator = new nb.xutils.Validator(em, rules, messages);
            return validator.validate(params);
		},
		save:function(){
			var self = this;
			var params = nb.uiTools.mapFields(self._panel_id + " div.box");
			if(!self._validate(params)){return;}
			params.zIndex*=1;
			nb.uiTools.closeEditDialogWin(self._panel_id);
			nb.rpc.customerMapViews.c("editCustomerMapProps", params).success(function(msg){
				nb.AlertTip.storeCookie(msg);
				pageReload();
			});
		},
		__init__:function(){
			var self = this;
			$("#customerMapListWidget").delegate("a[name=edit_props]", "click", function(){
				var li = $(this).closest("li");
				var mcUid = li.attr("mcuid");
				var title = li.attr("title");
				var zIndex = li.attr("zindex");
				
				var box = $(self._panel_id + " div.box");
				box.find("input[name=mcUid]").val(mcUid);
				box.find("input[name=title]").val(title);
				box.find("input[name=zIndex]").val(zIndex);
				nb.uiTools.showEditDialogWin(null, self._panel_id, {title:"编辑义拓朴图属性", width:500, height:200});
				
			});
			
			$(self._panel_id + " button.ok").bind("click", function(){
				self.save();
			})
		}
	}
	
	
	m.delCustomermapWidget = {
		del:function(mcUid){
			nb.rpc.customerMapViews.c("removeCustomerMap",{mcUid:mcUid}).success(function(msg){
				nb.AlertTip.storeCookie(msg);
				pageReload();
			});
			
		},
		__init__:function(){
			var self = this;
			 $("#customerMapListWidget").delegate("a[name=del_customer_map]", "click", function(){
			 	var li = $(this).closest("li");
			 	var mcUid = li.attr("mcuid");
			 	if(window.confirm("你确定要删除此拓朴图吗?")){
			 		self.del(mcUid);
			 	}
			 })
		}
	}
	
	
		
	$(document).ready(function(){
		
		m.customerMapListWidget.__init__();
		m.customerMapListWidget.reload();
		
		m.addCustomermapWidget.__init__();
		m.editCustomerMapPropsWidget.__init__();
		
		m.delCustomermapWidget.__init__();
		
	});
	
	$(document).ready(function(){
		
		//打开拓朴图编辑
		$("#customerMapListWidget").delegate("a[name=edit_customer_map]",'click',function(){
			var mcUid = $(this).closest("li").attr("mcUid");
			var src = "/viewer/customerMap/edit/" + mcUid;
			$("#map_iframe").attr("src", src);
			
			$("#customerMapListWidget>ul>li").removeClass("selected");
			$(this).closest("li").addClass("selected");
		});
		
		//打开拓朴图查看
		$("#customerMapListWidget").delegate("a[name=view_customer_map]",'click',function(){
			var mcUid = $(this).closest("li").attr("mcUid");
			var src = "/viewer/customerMap/view/" + mcUid;
			$("#map_iframe").attr("src", src);
			
			$("#customerMapListWidget>ul>li").removeClass("selected");
			$(this).closest("li").addClass("selected");
			
		});
		

		
		
		
	});
	
	
	
})(jQuery)
