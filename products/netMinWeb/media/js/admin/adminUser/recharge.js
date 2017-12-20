(function($) {
    var m = window.recharge= new nb.xutils.Observer();
       
    var _ds = null;
    var _conditions = null;
    var getDs = m.getDs = function() {
        if(_ds) return _ds;
        var ds = new kendo.data.DataSource({
            type : "json", pageSize : 50,
            transport : {
                read : nb.rpc.adminUserViews.rc("getNotCheckedRechargeForm"),
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
           m.rechargeDetailWidget._rowViewModel = data;
           m.rechargeDetailWidget.viewModel = kendo.observable(note);
           m.rechargeDetailWidget.reload();
        };
 
        var _columns = [
            { field : "", title : "选择",  width :70, template: '<input type="checkbox" class="formID"  formid="#=_id#" />', 
            headerTemplate: '<input type="checkbox" class="check-all" /><label for="check-all">全选</label>'},
            { field : "customer", title : "用户名", width : 100 },
            { field : "company", title : "公司名称", width : 100 },
            { field : "money", title : "当前账户余额", width : 100, template: "#=nb.xutils.showMoney(userMoney)#" }, 
            { field : "money", title : "申请充值金额", width : 100, template: "#=nb.xutils.showMoney(money)#" }, 
            { field : "saleUser", sortable : true, title : "销售人员", width : 100 },
            { field : "submitTime", title : "申请时间", width : 150, template : "#=nb.xutils.getTimeStr(submitTime * 1000)#" },
            { field : "status", title : "审批状态",  width : 100, template: "#=nb.xutils.formStatusD2C(status)#"}
        ];

        $("#data-grid").kendoGrid({
            dataSource : getDs(),
            change:onChange,
            height : 400,
            pageable:true,
            selectable : true,
            sortable : true,
            columns : _columns
        });

        return $("#data-grid").data("kendoGrid");
    };
    
    m.rechargeDetailWidget = {
        
        _panel_id:"#rechargeDetailWidget",
        viewModel:null,
        _render: function(){
            var self = this;
            $(self._panel_id).show();
            self.viewModel.formatsubmitTime = function(){
                return nb.xutils.getTimeStr(this.submitTime*1000);
            };
            
           self.viewModel.set("money", nb.xutils.ReDecimalPoint(self.viewModel.money, 2));
           self.viewModel.set("userMoney", nb.xutils.ReDecimalPoint(self.viewModel.userMoney, 2));
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
    };
    
    
    var changeFormStatus = function(flag){
        var uids = [];
        $("#rechargeWidget input.formID:checked").each(function(){
            uids.push($(this).attr("formid"));
         });
        if (uids.length == 0 ){
            confirm("请选择对应的行！");
            return;
        }
        if(flag == 1 ){
            if(!confirm("确定通过？")){return;}
        }else{
            if(!confirm("确定回退？")){return;}
        }
       
        nb.rpc.adminUserViews.c("changeRechargeFormStatus", {uids: uids, flag: flag})
        .success(function(msg){
            nb.AlertTip.info(msg);
            getDs().read();
        });
    };
    
    
        
    $(document).ready(function() {
         m.createGrid();
         
          m.rechargeDetailWidget.__init__();
         
         $("#rechargeWidget .opForm button[name=checkedForm]").bind("click", function(){
            // if(!confirm("确定通过？")){return;}
            changeFormStatus(1);
         });
         
         $("#rechargeWidget .opForm button[name=uncheckedForm]").bind("click", function(){
             //if(!confirm("确定不通过？")){return;}
             changeFormStatus(2);
         });
         
        
        $("#rechargeWidget input.check-all").click(function(){
            if(this.checked){
                $("#rechargeWidget input.formID ").each(function(){
                    $(this).prop("checked", true );
                });
                
            }else{
                $("#rechargeWidget input.formID ").each(function(){
                    $(this).prop("checked", false );  
                });
            }           
        });
        
        
      $(".query_tool_bar select[name=status]").bind("change",function(){
          var status = $(this).val();
          window.location.href = "/admin/getExtendDevices/?status="+ status;
      });
      
      $("a[action=add]").bind("click",function(){
      	var params = {edId:$(this).attr("ed")};
        if(window.confirm("您确定要为该用户添加吗？")){
        	nb.rpc.adminUserViews.c("extendDeviceAdmin", params)
	        .success(function(msg){
	            nb.AlertTip.storeCookie(msg);
	            location.reload();
    		});
        }else{
        	return;
        }
        
      })

      
      $("a[action=delete]").bind("click",function(){
      	var params ={edId:$(this).attr("ed")};
        if(window.confirm("您确定要删除该充值记录吗？")){
        	nb.rpc.adminUserViews.c("deleteExtendInfo", params)
	        .success(function(msg){
	            nb.AlertTip.storeCookie(msg);
	            location.reload();
    		});
        }else{
        	return;
        }         
      })
    
    });

})(jQuery);
