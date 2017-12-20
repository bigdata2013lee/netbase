(function($) {

    var m = window.shortcutCmd = {};
    var targetDevs = [];
    var pageLoad = function(){
        m.shortcutCmdListWidget.reload();
    };
    _validate=function(params){
        var self = this;
        var em = $(self._panel_id + " div.validateErrorMsg");
        var messages = {cmd:"命令是必填项", targetDevRef:"设备是必填项"};
        var rules = {cmd: "required", targetDevRef:"required"};
        var validator = new nb.xutils.Validator(em, rules, messages);
        return validator.validate(params);
    };
        
    m.shortcutCmdListWidget = nb.BaseWidgets.extend("BaseListWidget", {
        _panel_id:"#shortcutCmdListWidget",
        remoteMethod:"listCmds",
        remoteView:nb.rpc.shortcutCmdViews,
        getRemoteParams: function(){return {}},
        remove:function(uids){
            nb.rpc.shortcutCmdViews.c("removeCmd", {uids:uids}).success(function(msg){
               nb.AlertTip.auto(msg);
               pageLoad();
            });
        },
        executeCmd:function(uid){
            var loading = nb.uiTools.commLoading.insertTo("body");
            loading.css({"position":"fixed"});
            loading.find("span:first").css({"margin-top":"105px"});
            loading.find("span:first").html("正在发送远程命令，请稍后...");
            
            nb.rpc.shortcutCmdViews.c("executeCmd", {uid:uid}).success(function(msg){
               if(/^\w*warn:/.test(msg)){nb.AlertTip.auto(msg);nb.uiTools.commLoading.cancel("body");return;}
               nb.uiTools.commLoading.cancel("body");
               nb.uiTools.cmdInfo(msg);
            });
        },
        afterInit:function(){
            var self = this;
            $(self._panel_id + " .op_bar a[name=create]").bind("click", function(){
                m.addShortcutCmdWidget.show();
            });
            
            $(self._panel_id + " .op_bar a[name=edit]").bind("click", function(){
                var cmdUids_checkbox = $(self._panel_id + " input[name=cmdUids]:checked");
                if(cmdUids_checkbox.size() == 0) return;
                if(cmdUids_checkbox.size() > 1){nb.AlertTip.warn("请选择一个编辑的快捷命令，不能选择多条命令"); return};
                var dataUid = cmdUids_checkbox.closest("tr").attr("data-uid");
                var data = self.ds().getByUid(dataUid);
                if(!data){return;}
                data = data.toJSON();
                var model = {"cmdUid": data._id, title: data.title, cmd:data.cmd, targetDevRef:data.targetDev.ref};
                //console.info(model);
                m.editShortcutCmdWidget.show(model);
            });
            
            $(self._panel_id + " .op_bar a[name=remove]").bind("click", function(){
                var cmdUids_checkbox = $(self._panel_id + " input[name=cmdUids]:checked");
                if(cmdUids_checkbox.size() == 0) return;
                var uids = cmdUids_checkbox.map(function(){
                    var dataUid = $(this).closest("tr").attr("data-uid");
                    var data = self.ds().getByUid(dataUid);
                    return data._id;
                }).get();
                self.remove(uids);
            });
            
            $(self._panel_id).delegate(".execute_btn_div button", "click", function(){
                var cmdUid = $(this).attr("cmdUid");
                self.executeCmd(cmdUid);
            });
        }
    });
    
    
    m.addShortcutCmdWidget = {
        _panel_id:"#addShortcutCmdWidget",
        
        show:function(){
            var self = this;

            self.viewModel=kendo.observable({
                title:"未命名", cmd:"", targetDevRef:"", targetDevs:targetDevs
            });
            nb.uiTools.showEditDialogWin(self.viewModel, self._panel_id, {title:"创建快捷命令", width:500, height:300});
        },
        save:function(){
            var self = this;
            var params = self.viewModel.toJSON();
            delete params.targetDevs;
            var fg =self._validate(params);
            if(! fg ) return;
            var _remote = function(){
                nb.rpc.shortcutCmdViews.c("createCmd", params).success(function(msg){
                   nb.AlertTip.auto(msg);
                   pageLoad();
                });
            };
            
           nb.uiTools.closeEditDialogWin(self._panel_id);
           _remote();
        },
        _validate:_validate,
        __init__:function(){
            var self = this;
            $(self._panel_id + " .win_opbar button.ok").bind("click", function(){
                self.save();
            });
        }
    };
    
    
    m.editShortcutCmdWidget = {
        _panel_id:"#editShortcutCmdWidget",
        
        show:function(model){
            var self = this;
            var _model = $.extend({targetDevs:targetDevs},model)
            self.viewModel=kendo.observable(_model);
            nb.uiTools.showEditDialogWin(self.viewModel, self._panel_id, {title:"编辑快捷命令", width:400, height:220});
        },
        save:function(){
            var self = this;
            var params = self.viewModel.toJSON();
            delete params.targetDevs;
            var fg =self._validate(params);
            if(! fg ) return;
            nb.rpc.shortcutCmdViews.c("editCmd", params).success(function(msg){
               nb.AlertTip.auto(msg);
               pageLoad();
           });
           nb.uiTools.closeEditDialogWin(self._panel_id);
        },
        _validate:_validate,
        __init__:function(){
            var self = this;
            $(self._panel_id + " .win_opbar button.ok").bind("click", function(){
                self.save();
            });
        }
    };
    
    $(document).ready(function() {

       m.shortcutCmdListWidget.__init__();
       m.addShortcutCmdWidget.__init__();
       m.editShortcutCmdWidget.__init__();
       
       m.shortcutCmdListWidget.reload();
       nb.rpc.shortcutCmdViews.c("listTargetDevs").success(function(_targetDevs){
           targetDevs = _targetDevs;
       });
       
    });

})(jQuery);
