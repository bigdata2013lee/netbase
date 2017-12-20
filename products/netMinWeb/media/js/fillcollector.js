(function($){
	
	 m = nb.nameSpace("publicWidgets");
     m.fillCollectorSelectWidget = {
        
        _data: {"public":[], "private":[]},
        _render: function(){
            var self = this;
            var select = $("select#select_collector");
            
            if(! $.isEmptyObject(self._data["public"])){
	            var privateOptgroup = $('<optgroup label="内网收集器"></optgroup>').appendTo(select);
	            $.each(self._data["private"], function(i, item){
	                var option = $(nb.xutils.formatStr('<option value="{0}">{1}({2})</option>', item._id, item.title, item.host));
	                option.appendTo(privateOptgroup);
	            });
            }
            
            if(! $.isEmptyObject(self._data["public"])){
	            var publicOptgroup = $('<optgroup label="公网收集器"></optgroup>').appendTo(select);
	            $.each(self._data["public"], function(i, item){
	                var option = $(nb.xutils.formatStr('<option value="{0}">{1}({2})</option>', item._id, item.title, item.host));
	                option.appendTo(publicOptgroup);
	            });
            }
            
        },
        reload: function(){
            var self = this;
            if(!$("select#select_collector").size() > 0) return;
            self.componentType = $("select#select_collector").attr("component_type");
            nb.rpc.deviceViews.c("listCollectors",{componentType:self.componentType}).
            success(function(colls){
                self._data = colls;
                self._render();
            });
        },
        __init__:function(){
            var self = this;
            self.reload();
        }
        
    };
    
    
    $(document).ready(function(){
    	m.fillCollectorSelectWidget.__init__();
    })
    
    
})(jQuery)