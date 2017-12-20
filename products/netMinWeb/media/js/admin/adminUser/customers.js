(function($){
    
    var m = window.customersIndex= new nb.xutils.Observer();
    var _conditions = {};
    var _ds = null;
    var getDs = m.getDs = function() {
        if(_ds) return _ds;
        var ds = new kendo.data.DataSource({
            type : "json", pageSize : 50,
            transport : {
                read : nb.rpc.adminUserViews.rc("getAllUsers"),
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
            { field : "_id", title : "帐户编号",  width : 150},
            { field : "username", title : "用户名", width : 150 },
            { field : "company", title : "公司"},
            { field : "createTime", width:120, title : "注册日期", template : "#=nb.xutils.getTimeStr(createTime * 1000, true)#"},
            { field : "lastLoginTime", width:120, title : "最后登陆", template : "#=lastLoginTime#"},
            { field : "group", title : "类型", width:80, template:'#=nb.Render.userGroup(data.group)#'},
            { field : "money", width:120, title : "帐户余额",template : "#=nb.xutils.showMoney(money)#"},
            { title : "操作",width:120, template : '#if(data.group=="comm"){#<button name="toIdcUser" userId="#=data._id#">转IDC用户</button>#}#'},
            
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
                var username = $.trim($(self._panel_id + " input[name=username]").val());
                var company = $.trim($(self._panel_id + " input[name=company]").val());
                if(!$.isEmptyObject(username)){conditions['username'] = username}
                if(!$.isEmptyObject(company)){conditions['company'] = company}
                _conditions = conditions;
                getDs().read();
                
            });
        }
    }
    
    
    var toIdcUser = function(userId){
        if(!window.confirm("你确定要把此用户转为IDC用户吗？")){return;}  
        nb.rpc.adminUserViews.c("toIdcUser", {userId: userId})
        .success(function(msg){
            nb.AlertTip.info(msg);
            getDs().read();
        });
    };
    
    $(document).ready(function() {
         m.createGrid();
         queryWidget.__init__();
         $("#data-grid").delegate("button[name=toIdcUser]",'click', function(){
             var userId = $(this).attr("userId");
             toIdcUser(userId);
         });
    });    
    
})(jQuery);
