(function($) {
    var m = window.checkedRecharge = new nb.xutils.Observer();
    
    var _conditions = null;
    var _ds = null;
    var getDs = m.getDs = function() {
        if(_ds) return _ds;
        var ds = new kendo.data.DataSource({
            type : "json",
            pageSize : 20,
            transport : {
                read : nb.rpc.adminUserViews.rc("getAllRechargeForm"),
                parameterMap: function(){
                if (! _conditions) return;
                return  {
                      params : $.toJSON({
                            conditions : _conditions
                        })
                  }
               },
            }
    
        });
        _ds = ds;
        return _ds;
    };

    m.createGrid = function() {
        
        var onChange=function(arg){
           var dataUid = this.select().attr("data-uid");
           if(!dataUid || dataUid == "") return;
           
           var data = this.dataSource.getByUid(dataUid);
           var note = data.toJSON();
           m.customersDetailWigdet._rowViewModel = data;
           m.customersDetailWigdet.viewModel = kendo.observable(note);
           
           m.customersDetailWigdet.reload();
        };
        

 
        var _columns = [
        { field : "_id", title : "充值申请号",  width : 180}, 
        { field : "customer", title : "用户名",  width : 70}, 
        { field : "ownCompany", sortable : true, title : "公司名称", width : 50 }, 
        { field : "money", sortable : true,  title : "充值金额", width : 60,  template: "#=nb.xutils.showMoney(money)#"  }, 
        { field : "submitTime", sortable : true,  title : "申请时间", width : 120,  template: "#=nb.xutils.getTimeStr(submitTime*1000)#"},
        { field : "completeTime", sortable : true,  title : "审核时间", width :120,  template: "#=nb.xutils.getTimeStr(completeTime*1000)#"}, 
        { field : "adminUser", sortable : true,  title : "审核人", width :70 }, 
        { field : "status", sortable : true,  title : "审核状态", width : 70, template:"#= nb.xutils.formStatusD2C(status)#"}, 
        ];

        $("#data-grid").kendoGrid({
            dataSource : getDs(),
            change:onChange,
            height : 300,
            pageable:true,
            selectable : true,
            sortable : true,
            columns : _columns
        });

        return $("#data-grid").data("kendoGrid");
    };
    
    
    m.customersDetailWigdet = {
        
        _panel_id:"#customersDetailWidget",
        viewModel:null,
        _render: function(){
            var self = this;
            $(self._panel_id).show();
            self.viewModel.formatsubmitTime = function(){
                return nb.xutils.getTimeStr(this.submitTime*1000);
            };
            
            self.viewModel.set("money", nb.xutils.ReDecimalPoint(self.viewModel.money, 2));
       
           self.viewModel.formatcompleteTime = function(){
                return nb.xutils.getTimeStr(this.completeTime*1000);
            };
            
           self.viewModel.formatStauts = function(){
                return nb.xutils.formStatusD2C(this.status);
            };
            
           
            
            kendo.bind($(self._panel_id + " .box:first"), self.viewModel);
        },
          
        reload:function(){
            var self = this;
            self._render();
        },
        

        __init__:function(){
            
            var self = this;
            $(self._panel_id).hide();
            
            var box = $(self._panel_id +" .box:first");
           
        }  
    },
    
    //---------------------------------------------------------------------------------------------//
    
    $(document).ready(function() {
         m.createGrid();
         m.customersDetailWigdet.__init__();   
         
         $("#customer_query_conditions button[name=selectQueryBt]").bind("click", function(){
             _conditions = nb.xutils.setQueryConditions("#customer_query_conditions", true);
             getDs().read();
         });
         
    });

})(jQuery);
