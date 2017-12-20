(function($){
	var m = window.hostTree = new nb.xutils.Observer();
	var locTypeName = "Location";
	var orgTypeName = "DeviceClass";
	var moTypeName = "Device";
	var remoteView = nb.rpc.treeViewApi;
	var remoteMethod = "getHostTreeWithLocDataSource";
	var _panel_id="#device_class_tree";
	var _template = '#=item.title# <input type="hidden" name="#=item._type#" value="#=item._id#"/>  \
	#if(item.count>=0){#<span class="item_count"> #=item.count#</span>#}#';
	
	
	m.treeWidget = {
		_panel_id: _panel_id,
		__ds:null,
		ds: function(){
            var self = this;
            if(self.__ds){return self.__ds;}
            var ds = new kendo.data.HierarchicalDataSource({ data: self._data });
            self.__ds = ds;
            return ds;
		},
		_render: function(){
			var self = this;
			var  dataSource = self.ds();
			var treeView = $(self._panel_id).kendoTreeView({
				loadOnDemand: false,
				dataSource: dataSource,
				dataTextField: ["title"],
				dataSpriteCssClassField:"_type",
				template: kendo.template(_template),
				select: function(evt){
					
					var dataUid = $(evt.node).attr("data-uid");
					var data = this.dataSource.getByUid(dataUid);
					m.fireEvent("changeTreeNodeType", data._type, data.uname);
					
					if(data._type == orgTypeName){
						
				        var _pNode = data;
				        var _ownLocUid = null;
				        for(var i=0; i < 10; i++){//向上查找loc
				        	_pNode = _pNode.parentNode();
				        	if(!_pNode) break;
				        	if(_pNode._type == locTypeName){
				        		_ownLocUid = _pNode._id;
				        		break;
				        	}
				        	
				        }
	        
						m.fireEvent("selectOrgNode", data._id, data.uname, data.path, _ownLocUid);
					}
					else if(data._type == locTypeName){
						m.fireEvent("selectLocNode", data._id, data.title);
					}
					
				}
            });
            self.ds().data(self._data);
			
		},
		getTemplate: function(){},
		
		reload: function(){
			var self = this;
			remoteView.c(remoteMethod).
			success(function(data){
				self._data = data;
				self._render();
				m.fireEvent("afterRender");
			});

		}
	
	};
	

	
	m.on("afterRender", function(){
	    var ds = m.treeWidget.ds();
        
        /**
         * 选择正确的节点
         * @param {Object} node
         */
        var  _selectItem = function(){
			var locInputEl = $(_panel_id).find("input[value="+locUid+"][name="+locTypeName+"]");
			var orgInputEl = locInputEl.closest("li").find("input[value="+orgUid+"][name="+orgTypeName+"]");
			
			var locDataUid = locInputEl.closest("li").attr("data-uid");
			var orgDataUid = orgInputEl.closest("li").attr("data-uid");
			
			console.info(locDataUid,orgDataUid);
			
			
	        var orgNode = ds.getByUid(orgDataUid);
	        if(!orgNode) return;
	        orgNode.set("selected",true);
	        
	        var _pNode = orgNode;
	        for(var i=0; i < 10; i++){
	        	_pNode = _pNode.parentNode();
	        	if(!_pNode) break;
	        	_pNode.set("expanded",true);
	        	
	        }
	        	
        };
        
        window.setTimeout(function(){_selectItem();},10)
        
	});
	
	

	
	$(document).ready(function(){
		m.treeWidget.reload();
		
		
	});
	
})(jQuery);
