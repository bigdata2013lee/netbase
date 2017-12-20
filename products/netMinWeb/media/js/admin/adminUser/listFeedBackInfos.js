(function($){
    
    var m = window.listFeedBackInfos= new nb.xutils.Observer();
    var _conditions = {};
    var _ds = null;
    var getDs = m.getDs = function() {
        if(_ds) return _ds;
        var ds = new kendo.data.DataSource({
            type : "json", pageSize : 50,
            transport : {
                read : nb.rpc.adminUserViews.rc("listFeedBackInfos"),
                parameterMap: function(){
                  if (! _conditions) return;
                  return  {
                      params : $.toJSON({conditions : _conditions})
                  }
                },
            }
    
        });
        _ds = ds;
        return _ds;
    };
    
    
    m.createGrid = function() {
        
        var onChange=function(arg){
            //pass
        };
 
        var _columns = [
            { field : "infoTime", title : "时间",width: 150},
            { field : "feedBackUser", title : "用户名", width : 200 },
            { field : "feedBackEmail", title : "邮箱", width: 200},
            { field : "title", title : "反馈标题",  width : 180},
            { field : "feedBackContent", title : "反馈信息"}
        ];

        $("#data-grid").kendoGrid({
            dataSource : getDs(),
            change:onChange,
            height : 400,
            pageable:true,
            sortable : true,
            columns : _columns
        });

        return $("#data-grid").data("kendoGrid");
    };
    
    var queryWidget = {
        _panel_id: '#query_conditions',
        __init__: function(){
            var self = this;
            $(self._panel_id + " button.query").bind("click", function(){
                var conditions = {};
                var feedBackContent = $.trim($(self._panel_id + " input[name=feedBackContent]").val());
                if(!$.isEmptyObject(feedBackContent)){conditions['feedBackContent'] = feedBackContent}
                _conditions = conditions;
                getDs().read();
                
            });
        }
    }
    
    $(document).ready(function() {
         m.createGrid();
         queryWidget.__init__();
    });    
    
})(jQuery);
