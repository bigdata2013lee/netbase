(function($){
    
    var m = window.reportClsTree = new nb.xutils.Observer();
    var moTypeName = "Website";//Website
    var remoteView = nb.rpc.treeViewApi;
    var remoteMethod_site = "getWebsiteTreeDataSource";//getWebsiteTreeDataSource
    var remoteMethod_device = "getHostTreeDataSource";
    var remoteMethod_network = "getNetworkTreeDataSource";
    
    //var _panel_id="#report_tree";//website_tree 
    var _template = '#=item.title# <input type="hidden" name="#=item._type#" value="#=item._id#"/> #if(item.count>=0){#<span class="item_count"> #=item.count#</span>#}#';
    
    base_treeWidget = {
    	_panel_id:null,
        __ds:null,
        _data:[],
        ds: function(){
            var self = this;
            if(self.__ds){return self.__ds;}
            ds = new kendo.data.HierarchicalDataSource({ data: self._data });
            self.__ds = ds;
            return ds;
        },
		_render: function(){
            var self = this;
            self.ds().data(self._data);
            var dataSource = self._data;
            var treeView = $(self._panel_id).data("kendoTreeView");
            if(!treeView){
                var treeView = $(self._panel_id).kendoTreeView({
                	checkboxes: {
		                checkChildren: true
		            },
                    dataSource: dataSource,
                    dataTextField: ["title"],
                    dataSpriteCssClassField:"_type",
                    template: kendo.template(_template),
                    select: function(evt){
                        var dataUid = $(evt.node).attr("data-uid");
                        var data = this.dataSource.getByUid(dataUid);
                        m.fireEvent("changeTreeNodeType", data._type, data.uname);
                        
                        if(data._type == orgTypeName){
                            m.fireEvent("selectOrgNode", data._id, data.uname);
                        }
                        else if(data._type == moTypeName){
                            m.fireEvent("selectMoNode", data._id);
                        }

                    },
                });
            }
        },
        getTreeView:function(){
            var self = this;
            return $(self._panel_id).data("kendoTreeView");
        },
        reload: function(){ }
    };
    
    m.website_treeWidget = $.extend({}, base_treeWidget, {
        _panel_id:"#report_website_tree",        
        reload: function(){
            var self = this;
            var _classid="#WebSiteClassID";
             /** 统计mo对象数*/
            var setCount = function(dictObj){
                var count=0;
                if(!dictObj["items"] && dictObj._type == moTypeName) return 1;
                if(!dictObj["items"]) return 0;
                
                for(var i=0; i < dictObj["items"].length; i++){
                    count+=setCount(dictObj["items"][i]);
                }
                dictObj["count"] = count;
                return count;
            };
            var setChecked = function(dictObj){
            	var ids = $(_classid).val();            	
            	if(ids==null||ids.length==0){return;}            	
            	setCheckeds(dictObj,ids);
            };
            $(self._panel_id).bind("change", function() { 
				//插入选中项
				var checkedNodes = [],
	                treeView = $(self._panel_id).data("kendoTreeView"),
	                message;
	            checkedNodeIds(treeView.dataSource.view(), checkedNodes);	            		            
	            $(_classid).val(checkedNodes.join(","));			
			});
            read:remoteView.c(remoteMethod_site).
            success(function(data){
                data[0].expanded = true;
                setCount(data[0]);                
                setChecked(data[0]);
                self._data = data;
                self._render();
            });
        }
    });
    m.device_treeWidget = $.extend({}, base_treeWidget, {
        _panel_id:"#report_device_tree",        
        reload: function(){
            var self = this;
            var _classid="#DeviceClassID";
             /** 统计mo对象数*/
            var setCount = function(dictObj){
                var count=0;
                if(!dictObj["items"] && dictObj._type == moTypeName) return 1;
                if(!dictObj["items"]) return 0;
                
                for(var i=0; i < dictObj["items"].length; i++){
                    count+=setCount(dictObj["items"][i]);
                }
                dictObj["count"] = count;
                return count;
            };
            var setChecked = function(dictObj){
            	var ids = $(_classid).val();            	
            	if(ids==null||ids.length==0){return;}            	
            	setCheckeds(dictObj,ids);
            };
            $(self._panel_id).bind("change", function() { 
				//插入选中项
				var checkedNodes = [],
	                treeView = $(self._panel_id).data("kendoTreeView"),
	                message;
	            checkedNodeIds(treeView.dataSource.view(), checkedNodes);	
	            	            		            
	            $(_classid).val(checkedNodes.join(","));			
			});
            read:remoteView.c(remoteMethod_device).
            success(function(data){
                data[0].expanded = true;
                setCount(data[0]);                
                setChecked(data[0]);
                self._data = data;
                self._render();
            });
        }
    });
    m.network_treeWidget = $.extend({}, base_treeWidget, {
        _panel_id:"#report_network_tree",        
        reload: function(){
            var self = this;
            var _classid="#NetworkClassID";
             /** 统计mo对象数*/
            var setCount = function(dictObj){
                var count=0;
                if(!dictObj["items"] && dictObj._type == moTypeName) return 1;
                if(!dictObj["items"]) return 0;
                
                for(var i=0; i < dictObj["items"].length; i++){
                    count+=setCount(dictObj["items"][i]);
                }
                dictObj["count"] = count;
                return count;
            };
            var setChecked = function(dictObj){
            	var ids = $(_classid).val();            	
            	if(ids==null||ids.length==0){return;}            	
            	setCheckeds(dictObj,ids);
            };
            $(self._panel_id).bind("change", function() { 
				//插入选中项
				var checkedNodes = [],
	                treeView = $(self._panel_id).data("kendoTreeView"),
	                message;
	            checkedNodeIds(treeView.dataSource.view(), checkedNodes);		            
	            $(_classid).val(checkedNodes.join(","));			
			});
            read:remoteView.c(remoteMethod_network).
            success(function(data){
                data[0].expanded = true;
                setCount(data[0]);                
                setChecked(data[0]);
                self._data = data;
                self._render();
            });
        }
    });
    function setCheckeds(dictObj,ids){
        if(!dictObj["items"]) return;
        var objclasshtml = [];
        var spanobjclass = $("#_reportObjclass");
    	for(var i=0; i < dictObj["items"].length; i++){
            if((ids.indexOf(dictObj["items"][i]._id)>=0))
            {
            	dictObj["items"][i].checked = true;
            	objclasshtml.push(dictObj["items"][i].title);
            }
            else
            {
            	if(dictObj["items"][i]["items"]!=null&&dictObj["items"][i]["items"].length>0){
            		setCheckeds(dictObj["items"][i],ids);
            	}
            }
        }
        if($("#_reportObjclass")){
        	$("#_reportObjclass").html(objclasshtml.join(" "));
        }
        
    }
    
    function checkedNodeIds(nodes, checkedNodes) {
		for (var i = 0; i < nodes.length; i++) {
			if (nodes[i].checked) {
				if(nodes[i].uname!="devicecls"){
					if(nodes[i]._type=="NetworkClass")
					{
						if(nodes[i].uname==null){
							checkedNodes.push(nodes[i]._id);
						}
					}
					else{
						checkedNodes.push(nodes[i]._id);
					}
				}
			}
			if (nodes[i].hasChildren) {
				checkedNodeIds(nodes[i].children.view(), checkedNodes);
			}
		}   		
	}
    $(document).ready(function(){
        m.website_treeWidget.reload();
        m.device_treeWidget.reload();
        m.network_treeWidget.reload();
        
    });    
})(jQuery);
