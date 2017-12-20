(function($) {
    var m = window.customers = new nb.xutils.Observer();
    
    
    m.on("afterSuccessRechargeForCustomer", function(){
        
    });
    var _conditions = null;
    var _ds = null;
    var getDs = m.getDs = function() {
        if(_ds) return _ds;
        var ds = new kendo.data.DataSource({
            type : "json",
            pageSize : 20,
            transport : {
                read : nb.rpc.saleViews.rc("getUsers"),
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
        { field : "username", title : "用户名",  width : 100}, 
        { field : "ownCompany", sortable : true, title : "公司", width : 150 }, 
        { field : "contactPhone",  title : "联系电话", width : 130 }, 
        { field : "idcUser",  title : "IDC公司名称", width : 130 },
        { field : "money",  title : "当前账户余额", width : 130, template: "#=nb.xutils.showMoney(money)#" },
        {title:"操作", width:120, template:'<a href="javascript:" uid="#=_id#" name="rec">充值</a> | <a href="javascript:" uid="#=_id#" name="setEng">设置工程师</a>'}
        ];

        $("#data-grid").kendoGrid({
            dataSource : getDs(),
            change:onChange,
            height : 480,
            pageable:true,
            selectable : false,
            sortable : true,
            columns : _columns
        });

        return $("#data-grid").data("kendoGrid");
    };
    
   
    
    m.rechargeWidget = {
    	_panel_id:"#rechargeWidget",
        _render: function(){},
        reload:function(){},
        
         _validate:function(params){
            var self = this;
            var em = $(self._panel_id + " div.validateErrorMsg");
            var messages = {rechargeMoney:"充值金额格式不正确，请重新填写!(0~9999999)"};
            var rules = {rechargeMoney: {method:"regex", exp:/^[1-9]\d{0,6}$/}};
            var validator = new nb.xutils.Validator(em, rules, messages);
            return validator.validate(params);
            
        },
        save: function(){
            var self = this;
            var viewModel = $(self._panel_id).data("viewModel");
            var rechargeMoney = $(self._panel_id + " input[name=rechargeMoney]").val();
            rechargeMoney = $.trim(rechargeMoney);
            var rechargeInstructions =  $(self._panel_id + " textarea[name=rechargeInstructions]").val();
            rechargeInstructions = $.trim(rechargeInstructions);
            var  params = {customerUid: viewModel._id, rechargeMoney:rechargeMoney,rechargeInstructions: rechargeInstructions };
            if(!self._validate(params)){return false;}
            if(!confirm("确认提交申请！")){return false;}
            nb.rpc.saleViews.c("rechargeForCustomer", params).success(function(msg){
                nb.AlertTip.auto(msg);
                m.fireEvent("afterSuccessRechargeForCustomer");
            });
            return true;
        },
        __init__:function(){
        	var self = this;
        	$(self._panel_id + " .win_opbar button.ok").bind("click", function(){
        		var fg = self.save();
        		if(fg){
        			nb.uiTools.closeEditDialogWin(self._panel_id);
        		} 
        		
        	})
        }
    	
    }
    
    m._engineerListWidget=nb.BaseWidgets.extend("BaseListWidget", {
    	_panel_id:"#engineerListWidget",
        remoteMethod:"getEngineers",
        idcProviderId:"",
        remoteView:nb.rpc.engineerViews,
        getRemoteParams: function(){var self = this;return {idcProviderId:self.idcProviderId}},
    })
    m.setEngineerWidget = {
    	_panel_id:"#setEngineerWidget",
        _render: function(){},
        reload:function(){},
        save:function(){
        	var self = this;
            var viewModel = $(self._panel_id).data("viewModel");
            var engineerUid = $(self._panel_id + " input[name=engineerUid]:checked").val();
            var  params = {customerUid: viewModel._id, engineerUid:engineerUid};
            if(!confirm("确认修改工程师？")){return false;}
            nb.rpc.saleViews.c("setCustomerEngineer", params).success(function(msg){
                nb.AlertTip.auto(msg);
            });
            return true;
            
        },
        __init__:function(){
        	var self = this;
        	$(self._panel_id + " .win_opbar button.ok").bind("click", function(){
        		var fg = self.save();
        		if(fg){
        			nb.uiTools.closeEditDialogWin(self._panel_id);
        		}
        		
        	})
        }
    	
    }
    
    //---------------------------------------------------------------------------------------------//
    
    $(document).ready(function() {
         m.createGrid();
         m.rechargeWidget.__init__();
         m.setEngineerWidget.__init__();
         $("#customer_query_conditions button[name=selectQueryBt]").bind("click", function(){
             _conditions = nb.xutils.setQueryConditions("#customer_query_conditions", false);
             getDs().read();
         });
         
         $("#customersWidget").delegate("a[name=rec]", "click",function(evt){
         	var  duid = $(this).closest("tr").attr("data-uid");
         	var  data = getDs().getByUid(duid);
         	nb.uiTools.showEditDialogWin(data, m.rechargeWidget._panel_id,{title:"用户充值...",width:600, height:300});
         })
         
         $("#customersWidget").delegate("a[name=setEng]", "click",function(evt){
         	var  duid = $(this).closest("tr").attr("data-uid");
         	var  data = getDs().getByUid(duid);
         	nb.uiTools.showEditDialogWin(data, m.setEngineerWidget._panel_id,{title:"修改工程师...",width:600, height:300});
         	m._engineerListWidget.idcProviderId = data.idcProviderId;
         	m._engineerListWidget.reload();
         })
         
    });

})(jQuery);
