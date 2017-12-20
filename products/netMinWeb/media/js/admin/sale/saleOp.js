(function($){
    var m = window.saleOp = new nb.xutils.Observer();
     var _ds = null;
    var getDs = m.getDs = function() {
        if(_ds) return _ds;
        var ds = new kendo.data.DataSource({
            type : "json",
            pageSize : 20,
            transport : {
                read : nb.rpc.saleViews.rc("listSaleOpRecords"),
            }
        });
        _ds = ds;
        return _ds;
    };

    m.createGrid = function() {
        var _columns = [
        { field : "sale", title : "销售员",  width : 50}, 
        { field : "opTime", sortable : true, title : "操作时间", width : 100 }, 
        { field : "operation", sortable : true,  title : "操作摘要", width : 100 }, 
        { field : "opDetail",  title : "操作细节", width : 350 },  
        ];

        $("#data-grid").kendoGrid({
            dataSource : getDs(),
            height : 480,
            pageable:true,
            selectable : true,
            sortable : true,
            columns : _columns
        });
        return $("#data-grid").data("kendoGrid");
    };    
        
    $(document).ready(function(){
        m.createGrid();
    });
    
})(jQuery);
