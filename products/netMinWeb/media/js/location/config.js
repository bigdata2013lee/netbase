(function($){
	
	var m = new nb.xutils.Observer();
	
	var _orgUid = window.orgUid;
	var reloadPage=function(){window.location.reload();};

	m.locationsListWidget=nb.BaseWidgets.extend("BaseListWidget", {
		_panel_id:"#locationsListWidget",
		__body:"ul", 
		remoteView:nb.rpc.locationViews,
		remoteMethod:"listAllNodes",
		getRemoteParams: function(){ return {};},
		afterChange:function(){
			var self = this;
			$(self._panel_id + " li[locuid="+window.orgUid+"]").addClass("selected");
		},
		__init__:function(){
			var self = this;
			$(self._panel_id).delegate("a[name=listmos]","click", function(evt){
				window.location.href="/location/loc/"+$(this).closest("li").attr("locuid");
			})
		}
	})
	
	
	
	m.setLocation=function(){
		var orgUid = m.selectLocWidget.val();
		var mos = nb.devicesView.getSelectMos();
		var params = {orgUid:orgUid, mos:mos}
		nb.rpc.locationViews.c("setLocation", params).success(function(msg){
			nb.AlertTip.storeCookie(msg);
			reloadPage();
		});
		
	};
		
		
	
	m.selectLocWidget = {
		_panel_id:"#selectLocWin",
		_data:[],
		_render:function(){
			var self = this;
			select = $(self._panel_id + " select[name=location]");
			$.each(self._data, function(i, node){
				var option = $('<option value="'+node._id+'">'+node.title+'</option>');
				option.appendTo(select);
			});
			
		},
		reload:function(){
			var self = this;
			nb.rpc.locationViews.c("listAllNodes",{}).success(function(nodes){
				self._data=nodes;
				self._render();
			})
		},
		val:function(){
			var self = this;
			select = $(self._panel_id + " select[name=location]");
			return select.val();
		},
		
		show:function(){
			var self = this;
			nb.uiTools.showEditDialogWin(null, self._panel_id,{title:"重命名分组", width:400});
		},
		__init__:function(){
			var self = this;
			self.reload();
			$(self._panel_id + " button.ok:first").bind("click", function(){
				m.setLocation();
			});
			
		}
	}
	


	m.editLocWidget={
		_panel_id:"#renameLocWin",
		_validate_for_rename:function(params, winId){
			
			var em = $(winId + " div.validateErrorMsg");
            var messages = {title:"标题为必填项，请重新输入(中文\数字\字母\_ 2~16个字符)"};
            var rules = {title: {method:"regex", exp:/^[0-9a-zA-Z_\u4e00-\u9fa5]{2,16}$/}};
            var validator = new nb.xutils.Validator(em, rules, messages);
            return validator.validate(params);
			
		},
		renameLoc:function(){
			var self = this;
			
			var params = nb.uiTools.mapFields("#renameLocWin>div.box");
			var _v = self._validate_for_rename(params, "#renameLocWin");
			if(! _v)return;
			
			nb.rpc.locationViews.c("renameLoc", params).success(function(msg){
				nb.AlertTip.storeCookie(msg);
				nb.uiTools.closeEditDialogWin("#renameLocWin");
				reloadPage();
			});
		},
		
		addLoc:function(){
			var self = this;
			
			var params = nb.uiTools.mapFields("#addLocWin>div.box");
			var _v = self._validate_for_rename(params, "#addLocWin");
			if(! _v)return;
			
			nb.rpc.locationViews.c("addLoc", params).success(function(msg){
				nb.AlertTip.storeCookie(msg);
				nb.uiTools.closeEditDialogWin("#addLocWin");
				reloadPage();
			});
		},
		
		deleteLoc:function(uid){
			if(!window.confirm("你确定要删除此分组?")) return;
			nb.rpc.locationViews.c("delLoc", {uid:uid}).success(function(msg){
				nb.AlertTip.storeCookie(msg);
				window.location.href="/location/"
			});
		},
		__init__:function(){
			var self = this;
			$("#locationsListWidget").delegate("li a[name=edit]","click", function(){
				var title = $(this).closest("li").attr("title");
				var locUid = $(this).closest("li").attr("locuid");
				var obj = kendo.observable({title:title, locUid:locUid});
				nb.uiTools.showEditDialogWin(obj, "#renameLocWin",{title:"重命名分组", width:400});
			});
			
			$("a[name=add_location]").bind("click", function(){
				nb.uiTools.showEditDialogWin(null, "#addLocWin",{title:"添加新分组", width:400});
			});
			
			$("#locationsListWidget").delegate("li a[name=delete]","click", function(){
				var locUid = $(this).closest("li").attr("locuid");
				self.deleteLoc(locUid);
			});
			$("#renameLocWin .win_opbar button.ok").bind("click", function(){self.renameLoc()});
			$("#addLocWin .win_opbar button.ok").bind("click", function(){self.addLoc()});
		}
	};
	$(document).ready(function(){

		
		$("#mright-panel").delegate("a[name=setLocation]", "click", function(){
			if($.isEmptyObject(nb.devicesView.getSelectMos())){
				nb.AlertTip.auto("warn:未选择监控对象");
				return;
			}
			m.selectLocWidget.show()
		});
		
		
		m.selectLocWidget.__init__();
		m.editLocWidget.__init__();
		
		m.locationsListWidget.__init__();
		m.locationsListWidget.reload();
		
		

	})
	
	
})(jQuery)


















































































