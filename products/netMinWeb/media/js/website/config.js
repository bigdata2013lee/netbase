(function($){
    
    var m = window.websiteConfig = {};
    m._selectedClsId = null;
    
    m.pageReload = function(){
        websuteClsTree.treeWidget.reload();
    };
    
    websuteClsTree.on("changeTreeNodeType", function(type, uname){
        $("#tree_op_bar .box").hide();
        $("#tree_op_bar .box[for_type="+type +"]").show();
        
        if(type=="WebSiteClass" && uname == "websitecls"){
            $("#tree_op_bar .box a[for_root=1]").show();
            $("#tree_op_bar .box a[for_root=0]").hide();
        }
        else if(type=="WebSiteClass" && uname != "websitecls"){
            $("#tree_op_bar .box a[for_root=1]").hide();
            $("#tree_op_bar .box a[for_root=0]").show();
        }
        
        
       $(".panel.swich").hide();
    });
    
    
    websuteClsTree.on("selectOrgNode", function(clsId, uname){
        m._selectedClsId = clsId;
    });
    
    websuteClsTree.on("selectMoNode", function(id){
        m._selectedWebsiteId = id;
        $("#editWebsiteWidget").show();
        m.editWebsiteWidget.reload();
    });    
    
        
    m.addWebsiteWidget = {
        _panel_id: "#addWebsiteWidget", 
        viewModel: kendo.observable({
          "booleans" : [{text:"是", val:"true"},{text:"否", val:"false"}],
          "caseSensitive": "false",
          "description": "",
          "hostName": "",
          "httpPassword": "",
          "httpUsername": "",
          "invert": "false",
          "ipAddress": null,
          "onRedirect": "",
          "port": 80,
          "regex": "",
          "timeout": 10,
          "title": "",
          "tryCount": 2,
          "url": "/",
          "useSsl": "false"
        }),
        _render: function(){
            var self = this;
            kendo.bind($(self._panel_id + " .box:first"), self.viewModel);
        },
        _validate:function(medata){
            var self = this;
            var em = $(self._panel_id + " div.validateErrorMsg");
            var messages = {hostName:"域名或主机IP地址必须填写其中一项信息", ipAddress:"你输入的Ip地址不正确，请重新填写"}
            var rules = { 
                hostName: function(val){
                	if(!nb.xutils.isEmpty(medata.hostName) && !nb.xutils.isValidUrl(medata.hostName)){
            			messages.hostName = "域名填写不正确，请重新输入";
            			return false;
                	}
                    return !nb.xutils.isEmpty(medata.hostName) ||  !nb.xutils.isEmpty(medata.ipAddress);
                },
                ipAddress: {method:"norequired", rule:"ip"}
            };
            var validator = new nb.xutils.Validator(em, rules, messages);
            return validator.validate(medata);
            
        },
        save:function(){
            var self = this;
            var medata = self.viewModel.toJSON(); 
            
            delete medata.booleans;
            medata.caseSensitive = nb.xutils.val2boolean(medata.caseSensitive);
            medata.useSsl = nb.xutils.val2boolean(medata.useSsl);
            medata.invert = nb.xutils.val2boolean(medata.invert);
            
            if(!self._validate(medata)){return;}
           
            var _remote = function(){
                nb.rpc.websiteViews.c("addWebsite", {clsId: m._selectedClsId, medata:medata}).
                success(function(msg){
                     nb.AlertTip.auto(msg);
                     if(/^auth_warn/gi.test(msg)) return;
                     if(/^warn/gi.test(msg)) return;
                     m.pageReload();
                });
            }
            
            _remote();
        },
        delWebsite: function(){
            var self = this;
            if(!confirm("你确定要删除此站点吗?")) return;
            nb.rpc.websiteViews.c("delWebsite", {uid: m._selectedWebsiteId}).
            success(function(msg){
                 nb.AlertTip.auto(msg);
                 m.pageReload();
            });
        },
        
        __init__:function(){
            var self = this;
            $(self._panel_id + " .op_bar a[name=save]").bind("click", function(){
                self.save();
            });
            $(self._panel_id).hide();
            self._render();
            
            $("#tree_op_bar a[name=addWebsite]").bind("click", function(){
                 $(self._panel_id).show();
            });
            $("#tree_op_bar a[name=delWebsite]").bind("click", function(){
                 self.delWebsite();
            });
            
        }
    };
    
        
    m.editWebsiteWidget = {
        _panel_id: "#editWebsiteWidget", 
        viewModel: kendo.observable({
        }),
        _render: function(){
            var self = this;
            kendo.bind($(self._panel_id + " .box:first"), self.viewModel);
        },
        _validate:function(medata){
            var self = this;
            var em = $(self._panel_id + " div.validateErrorMsg");
            var messages = {hostName:"域名或主机IP地址必须填写其中一项信息", ipAddress:"你输入的Ip地址不正确，请重新填写"}
            var rules = {
                hostName: function(val){
                	if(!nb.xutils.isEmpty(medata.hostName) && !nb.xutils.isValidUrl(medata.hostName)){
            			messages.hostName = "域名填写不正确，请重新输入";
            			return false;
                	}
                    return !nb.xutils.isEmpty(medata.hostName) ||  !nb.xutils.isEmpty(medata.ipAddress);
                },
                ipAddress: {method:"norequired", rule:"ip"}
            };
            var validator = new nb.xutils.Validator(em, rules, messages);
            return validator.validate(medata);
            
        },
        openThresholdConfigWin:function(moUid, moType){
            nb.uiTools.showEditDialogWin(null, "#thresholdConfigWin", {width:1000, height:400, title:"阀值配置..."});
            m.thresholdConfigWinWidget._moUid = moUid;
            m.thresholdConfigWinWidget._moType = moType;
            m.thresholdConfigWinWidget.reload();
        },
        save:function(){
            var self = this;
            var medata = self.viewModel.toJSON(); 
            var uid = medata._id;
            delete medata._id;
            
            delete medata.booleans;
            medata.caseSensitive = nb.xutils.val2boolean(medata.caseSensitive);
            medata.useSsl = nb.xutils.val2boolean(medata.useSsl);
            medata.invert = nb.xutils.val2boolean(medata.invert);
            
            if(!self._validate(medata)){return;}
            nb.rpc.websiteViews.c("editWebsite", {uid: uid, medata:medata}).
            success(function(msg){
                 nb.AlertTip.auto(msg);
                 if(/^warn/gi.test(msg)) return;
                 m.pageReload();
            });
        },

        reload: function(){
            var self  = this;
            $(self._panel_id + " div.validateErrorMsg").hide();
            nb.rpc.websiteViews.c("getWebsite",{uid: m._selectedWebsiteId}).
            success(function(website){
                website.booleans = [{text:"是", val:"true"},{text:"否", val:"false"}];
                website.caseSensitive = nb.xutils.val2booleanStr(website.caseSensitive);
                website.useSsl = nb.xutils.val2booleanStr(website.useSsl);
                website.invert = nb.xutils.val2booleanStr(website.invert);
                
                self.viewModel = kendo.observable(website);
                self._render();
            });
        },
        __init__:function(){
            var self = this;
            $(self._panel_id + " .op_bar a[name=save]").bind("click", function(){
                self.save();
            });
            $(self._panel_id).delegate("a[name=configThreshold]", "click", function(){
                var moUid = m._selectedWebsiteId
                var moType = "Website";
                self.openThresholdConfigWin(moUid, moType);
            });
            $(self._panel_id).hide();
        }
    };
    
 
 
    m.addWebsiteClsWidget = {
        _panel_id: "#addWebsiteClsWidget", 
        viewModel: kendo.observable({
          "uname": "", "title": ""
        }),
        _render: function(){
            var self = this;
            kendo.bind($(self._panel_id + " .box:first"), self.viewModel);
        },
        _validate:function(params){
            var self = this;
            var em = $(self._panel_id + " div.validateErrorMsg");
            var messages = {uname:"名称格式不正确，请输入4-16位的字符"};
            var rules = {  uname: {method:"regex", exp:/^\w{4,16}$/} };
            var validator = new nb.xutils.Validator(em, rules, messages);
            return validator.validate(params);

        },
        save:function(){
            var self = this;
            var params = self.viewModel.toJSON();
            nb.xutils.trimObj(params);
            if(!self._validate(params)) return;
            
            nb.rpc.websiteViews.c("addWebsiteClass", params).
            success(function(msg){
                nb.AlertTip.auto(msg);
                m.pageReload();
            });
        },
        
        deleteCls:function(){
            if(!confirm("你确定要删除此分类吗？")) return;
            nb.rpc.websiteViews.c("delWebsiteClass", {clsId: m._selectedClsId}).
            success(function(msg){
                nb.AlertTip.auto(msg);
                m.pageReload();
            });
        },
        renameCls:function(){
            var treeView = websuteClsTree.treeWidget.getTreeView();
            var li = treeView.select();
            var dataUid = li.attr("data-uid");
            var data = treeView.dataSource.getByUid(dataUid);
            var title = window.prompt("输入新的名称", data.title);
            title = $.trim(title);
            if(nb.xutils.isEmpty(title)) return;
            nb.rpc.websiteViews.c("renameWebsiteClass", {clsId: m._selectedClsId, title:title}).
            success(function(){
                data.set("title",title);
            });
            
        },
        __init__:function(){
            var self = this;
            $(self._panel_id + " .op_bar a[name=save]").bind("click", function(){
                self.save();
            });
            $(self._panel_id + " .op_bar  a[name=deleteCls]").bind("click", function(){
                self.deleteCls();
            });
           
            
            $(self._panel_id).hide();
            self._render();
            
            var treeOpbar = $("#tree_op_bar");
            treeOpbar.find("a[name=addWebsiteCls]").bind("click", function(){
                 $(self._panel_id).show();
            });
            
            treeOpbar.find("a[name=deleteCls]").bind("click", function(){
                self.deleteCls();
            });
            
            treeOpbar.find("a[name=rename]").bind("click", function(){
                self.renameCls();
            });
        }
    };
    
    //弹出窗-阀值配置
    m.thresholdConfigWinWidget= nb.BaseWidgets.extend("thresholdConfigWidget",{
        _panel_id: "#thresholdConfigWin",
        _getMoUid: function(){return null},
        _moType:null
    });
    
    $(document).ready(function(){
        $("#tree_op_bar .box a").bind("click", function(){
            $(".panel.swich").hide();
        });
        
        m.addWebsiteWidget.__init__();
        m.addWebsiteClsWidget.__init__();
        m.editWebsiteWidget.__init__();
        m.thresholdConfigWinWidget.__init__();
    });
    
})(jQuery);
