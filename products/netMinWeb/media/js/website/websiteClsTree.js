(function($){
    
    var m = window.websuteClsTree = new nb.xutils.Observer();
    var cookieName = "websiteTreeViewStatusCache";
    var orgTypeName = "WebSiteClass";
    var moTypeName = "Website";
    var remoteView = nb.rpc.treeViewApi;
    var remoteMethod = "getWebsiteTreeDataSource";
    var _panel_id="#website_tree";
    var _template = '#=item.title# <input type="hidden" name="#=item._type#" value="#=item._id#"/> #if(item.count>=0){#<span class="item_count"> #=item.count#</span>#}#';
    var __storeStatusCache__ = function(){};
    
    m.treeWidget = {
        _panel_id:_panel_id,
        __ds:null,
        _data:[],
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
            
            var treeView = $(self._panel_id).data("kendoTreeView");
            if(!treeView){
                var treeView = $(self._panel_id).kendoTreeView({
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
                    collapse: function(){__storeStatusCache__()},
                    expand: function(){__storeStatusCache__()}
                });
            }
             self.ds().data(self._data);
            
            
        },
        getTreeView:function(){
            var self = this;
            return $(self._panel_id).data("kendoTreeView");
        },

        reload: function(){
            var self = this;
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
            
            remoteView.c(remoteMethod).
            success(function(data){
                data[0].expanded = true;
                setCount(data[0]);
                self._data = data;
                self._render();
                m.fireEvent("afterRender");
            });

        }
        
    };
    
    
    //记录折叠状态到cookie缓存中
    var storeStatusCache = function(){
            var ds = m.treeWidget.ds();
            var root = ds.data()[0];
            var statusCache = {};
            
            var  _reStatus = function(node){
                if(node._type != orgTypeName) return;
                statusCache[node._id] = node.expanded || false;
                if(!node.hasChildren) return;
                $.each(node.children.data(), function(i, cNode){
                    _reStatus(cNode);
                });
            };
            
            _reStatus(root);
            $.cookie(cookieName, $.toJSON(statusCache), {expires:3, path:"/"});
            
    };
    
    m.on("afterRender", function(){
        var statusCache = $.cookie(cookieName);
        if($.isEmptyObject(statusCache)){statusCache = "{}";}
        statusCache = $.evalJSON(statusCache);
        var ds = m.treeWidget.ds();
        var root = ds.data()[0];
        
        //恢复折叠状态
        var  _reStatus2 = function(node){
            if(node._type != orgTypeName) return;
            var expanded = statusCache[node._id] || false;
            if(!node.hasChildren) return;
            if(node._id !=root._id){//忽略根节点
                node.set("expanded", expanded);
            }
            $.each(node.children.data(), function(i, cNode){
                _reStatus2(cNode);
            });
        };
        
        _reStatus2(root);
        
        /**
         * 选择正确的节点
         * @param {Object} node
         */
        var  _selectItem = function(node){
            if(node._id == window.orgUid || node._id == window.moUid){
                node.set("selected", true);return;
            }
           if(node.items && node.items.length > 0){
                $.each(node.items, function(i, cNode){
                    _selectItem(cNode);
                });
            }
        };
        
        _selectItem(root);
        
        __storeStatusCache__ = function(){storeStatusCache()}; //after render 绑定折叠记录状态
    });
    
    
    m.on("changeTreeNodeType", function(){
        storeStatusCache();
    });
    
    $(document).ready(function(){
        m.treeWidget.reload();
    });
    
    
})(jQuery);
