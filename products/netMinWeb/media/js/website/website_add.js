(function($){
    var m = new nb.xutils.Observer();


    var openCptSelectWin = function(){
      
      $("div.cpt_item_add_btn a").bind("click", function(){
          nb.uiTools.showEditDialogWin(null, "#cptSelectWin", {title:"选择监测点", width:900, height:400})
      })
        
    };
    
    var setCptSelect=function(cpts){
        var cptItemBox = $("div.cpt_item_box").html("");
        $.each(cpts, function(i, cpt){
            var spanItem = nb.xutils.formatStr('<span class="cpt_item" ss="{1}" cptuid="{0}">{2}</span>', cpt.pid, cpt.ss, cpt.title);
            cptItemBox.append(spanItem);
        })
        
    };
    
    var getCpts=function(){
        var cptUids = [];
        $("div.cpt_item_box span.cpt_item").each(function(){
            cptUids.push($(this).attr("cptuid"));
        });
        
        return cptUids;
    };
    
    var sureCptSelect=function(){
        $("#cptSelectWin .win_opbar button.ok").bind("click", function(){
            var cpts = mapObjPage.getSelectCollPoints();
            if(cpts.length > mapObjPage.max){return}
            console.info(cpts);
            setCptSelect(cpts);
            nb.uiTools.closeEditDialogWin("#cptSelectWin");
            
        });
        
        
        
    };
    
    
    m.addWebsiteWidget = {
        _panel_id:"#addWebsiteWidget",
        _validate:function(params){
            var self = this;
            var em = $(self._panel_id + " div.validateErrorMsg");
            var messages = {"hostName":"请填写正确的域名/IP", cptUids:"请选择至少一个收集点"};
            var rules = {
                hostName:function(val){
                    var v1 = nb.xutils.isValidUrl(val);
                    var v2 = nb.xutils.isValidIp(val);
                    return  v1 || v2;
                },
                port:"port",
                cptUids:function(vals){return vals && vals.length > 0;}
            };
            var validator = new nb.xutils.Validator(em, rules, messages);
            return validator.validate(params);
        },
        
        saveConf:function(){
            var self = this;
            var params = nb.uiTools.mapFields(self._panel_id + " div.box");
            nb.xutils.trimObj(params);
            params.useSsl = nb.xutils.val2boolean(params.useSsl);
            params.cptUids = getCpts();
            console.info(params);
            if(! self._validate(params)){ return; }
            
            nb.rpc.websiteViews.c("addWebsite", {medata:params})
            .success(function(msg){
                nb.AlertTip.storeCookie(msg);
                window.location.href = "/website/index/";
            })
            
            
        },
        
        __init__:function(){
            var self = this;
            $(self._panel_id + " .op_bar a").each(function(){
                $(this).bind("click",function(){ self[$(this).attr("action")](); })
            }); //end bind  click-->action
        }
    };
    
    
    $(document).ready(function(){
        openCptSelectWin();
        sureCptSelect();
        
        m.addWebsiteWidget.__init__();
    })
            
})(jQuery)
