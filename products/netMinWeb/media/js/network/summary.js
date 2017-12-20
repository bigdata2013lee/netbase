(function($){

    var m = nb.nameSpace("summary");
    importCss("/media/css/summary.css");
    
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
        _countInfo: function(info){
            var self = this;
            var _xcount = 0;
            var f = function(subInfo){
                var obj = {};
                obj.goods = subInfo[0];
                obj.bads = subInfo[1];
                obj.unknowns = subInfo[2];
                obj.allCount = obj.goods + obj.bads + obj.unknowns;
                if(obj.allCount > 0){_xcount+=1}
                obj.score = window.parseInt(subInfo[3]);
                
                if(obj.score>=70){obj.statusColor="#14A006"; }
                else if(obj.score>=40){obj.statusColor="#1279BC"; }
                else if(obj.score<=40){obj.statusColor="#D90000"; }
                return obj;
            }
            
            
            self._data = {devices: f(info.devices), interfaces: f(info.interfaces)}
            
            if(!_xcount){_xcount = 1;}
            self._data.score = (self._data.devices.score +  self._data.interfaces.score)/_xcount;
            if(jQuery.isNumeric(self._data.score)){
                self._data.score =  parseInt(self._data.score);
            }
            if(self._data.score>=70){self._data.statusColor="#14A006"; }
            else if(self._data.score>=40){self._data.statusColor="#1279BC"; }
            else if(self._data.score<=40){self._data.statusColor="#D90000"; }
            
        },
        reload:function(){
            var self = this;
            nb.rpc.networkViews.c("getSummaryInfo")
            .success(function(info){
                self._countInfo(info);
                self._render();
            });
        
        },
        __init__:function(){
          var self = this;
          self.reload();
        }
    
    };
    
    $(document).ready(function(){
        m.summaryWidget.__init__();
    });
    
})(jQuery);