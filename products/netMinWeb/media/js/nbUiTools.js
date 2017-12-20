(function($){
    var m = nb.nameSpace("uiTools");
    
    
    /**
     *时间单位条 
     */
    m.TimeUnitBar = nb.Class({
        __init__: function(widget){
            var el = this.__initUi__($(widget._panel_id + " div.box:first"));
            this.widget = widget; 
            var self = this;
            if(!widget.timeUnit) widget.timeUnit = 'day';
            $(el).find(">span").bind("click", function(){
                if($(this).is(".selected")) return;
                $(this).siblings().removeClass("selected");
                $(this).addClass("selected");
                var val = $(this).attr("value");
                self.setRange(val);
            });
        },
        
        __initUi__: function(widgetBoxEl){
            var html = '<div class="timeRangeBar"><span value="day" class="selected"> 天 </span> \
            <span value="week"> 周 </span><span value="month"> 月 </span></div>';
                
            var el = $(html).insertBefore($(widgetBoxEl));
            return el;
        },
    
        setRange: function(r){
            this.widget.timeUnit = r;
            this.widget.reload();
        }
    });
    
    
    
    m.TimeRangeBar = nb.Class({
        __init__: function(widget){
            var el = this.__initUi__($(widget._panel_id + " div.box:first"));
            this.widget = widget; 
            var self = this;
            
            $(el).find(">span").bind("click", function(){
                if($(this).is(".selected")) return;
                $(this).siblings().removeClass("selected");
                $(this).addClass("selected");
                var val = $(this).attr("value") * 1;
                self.setRange(val);
            });
        },
        
        __initUi__: function(widgetBoxEl){
            var html = '<div class="timeRangeBar"><span value="3600" class="selected">小时</span> \
            <span value="86400"> 天 </span><span value="604800"> 周 </span></div>';
                
            var el = $(html).insertBefore($(widgetBoxEl));
            return el;
        },
    
        setRange: function(r){
            this.widget.timeRange = r;
            this.widget.reload();
        }
    });
    
    m.validatePassword = function(msg, callback){
        //button 事件返回false,能取消关闭
        if(!callback){callback = function(){}}
        if(! msg ) {msg = "";}
        var _callback = function(){
            var pwd = $("#dialog_validte_password").val();
            pwd=$.md5(pwd);
            $("#dialog_validte_password").val("");
            if(nb.xutils.isEmpty(pwd)) return false;
            var fg = false;
            nb.rpc.userApi.c("validatePassword", {pwd:pwd}, "json", false).success(function(rs){ fg = rs; });
            
            if(! fg){nb.AlertTip.warn("验证密码失败! 无法继续操作"); return;}
            if(fg){
                callback();
            }
        }
        
        msg += '<div style="margin-top:10px;">请输入确认密码: <input  type="password" id="dialog_validte_password" style="height:22px;"/></div>';
        var zdialog = $.Zebra_Dialog(msg,{
                'type':     'information',
                'title':    '确认',
                'overlay_close':false,
                'overlay_opacity':0.1,
                'width':420,
                'buttons':  [{caption: '确认', callback: _callback}, '取消']
        });
        return zdialog;
    };
    
    m.confirm = function(msg, callback){
        if(! msg ) {msg = "请确认你的操作";}
        if(!callback){callback = function(){}}
        var zdialog = $.Zebra_Dialog(msg,{
                'type':   'question',
                'title':    '确认',
                'overlay_close':false,
                'overlay_opacity':0.1,
                'width':420,
                'buttons':  [{caption: '确认', callback: callback}, '取消']
        });
        return zdialog;
    };
    
    m.cmdInfo = function(msg, callback){
        var _msg = '<div style="max-height:400px; overflow:auto;"><pre>'+msg+"</pre></div>";
        if(!callback){callback = function(){}}
        var zdialog = $.Zebra_Dialog(_msg,{
                'type':   false,
                'title':    '输出',
                'overlay_close':false,
                'overlay_opacity':0.1,
                'width':600,
                'buttons':  []
        });
        return zdialog;
    };
    
    m.wellcomeHelp = function(){
    	var cookieName = "wellcomeHelpKnowed";
    	var cookieKnowed = $.cookie(cookieName);
    	var kVal = "knowed";
    	if(cookieKnowed == kVal ) return;
    	var mesg = '<strong>欢迎登陆网脊运维通</strong><br/><br/>我是新手，不会配置，不知道如何添加监控设备,<br><b>我要获得帮助！</b>';
    	var knowed = function(){
			$.cookie(cookieName,kVal, {expires:7, path:"/"}); 
    	};
    	var openHelpPage = function(){
    		window.open("/help/help_center_zuji.html");
    	}
    	var dialog = new $.Zebra_Dialog(mesg, {
		    'modal': false,
		    'width':500,
		    //'position': ['right - 0', 'bottom + 0'],
		    buttons:[{caption: '知道了,勿扰', callback: knowed}, {caption: '一切从帮助开始 !', callback: openHelpPage}]
		});
		
		return dialog;
    	
    }
    
	m.clearBillingUid = function(){
		$("#billingUid_text").html("");
		$("#billingUid_val").val("");
	}     
	
	m.getBillingUid = function(){
		return $("#billingUid_val").val();
	}    

    //-----------------------------------loading ui-----------------------------------------//
    var _LoadingOptions = {
        spanStyle:'background:url(/media/images/nbloading.gif) no-repeat; padding-left:30px; margin-top:40px; line-height:22px;display:inline-block;',
        tipStr:"正在加载，请稍后..."
    };
    m.panelLoading = {
        insertTo: function(el){
            var loading = $(el).find(">div.loading");
            if(loading.size() == 0){
                var html ='<div class="loading"><span style="{0}">{1}</span></div>';
                html = nb.xutils.formatStr(html, _LoadingOptions.spanStyle, _LoadingOptions.tipStr);
                loading = $(html).appendTo($(el));
            }
            var timer = loading.data("timer");
            window.clearTimeout(timer);
            timer = window.setTimeout(function(){loading.hide();}, 1000*60);
            loading.show();
            loading.data("timer", timer);
        },
        cancel: function(el){
             var loading = $(el).find(">div.loading");
             loading.hide();
        }
    };
    
    m.commLoading = {
        insertTo: function(el, text){
            var loading = $(el).find(">div.loading");
            if(loading.size() == 0){
                var html ='<div class="loading"><span style="{0}">{1}</span></div>';
                html = nb.xutils.formatStr(html, _LoadingOptions.spanStyle, _LoadingOptions.tipStr);
                loading = $(html).appendTo($(el));
            }
            $(el).css({position: "relative"});
            loading.css({"position":"fixed"});
            
            var timer = loading.data("timer");
            window.clearTimeout(timer);
            timer = window.setTimeout(function(){loading.hide();}, 1000*60);
            loading.show();
            loading.data("timer", timer);
            
            if(text){
	            loading.find("span:first").html(text);
            }
            return loading;
        },
        cancel: function(el){
             var loading = $(el).find("div.loading");
             loading.hide();
        }
    };
    

    //----------------------------------dialog win--------------------------------------------------------//
    m.showEditDialogWin = function(observer, winId, options) {
        var _options = {
            top:20,
            left:30,
            modal : true,
            title : " ",
            height : 200,
            width : 300,
            resizable:false,
            actions : ["Close"]
        };

        $.extend(_options, options || {});
        var win = $(winId);
        if (!win.data("kendoWindow")) {
            win.kendoWindow(_options);
            win.find('button.cancel:first').bind('click', function() {
                win.data("kendoWindow").close();
            });
            
            win.show();
        }
        if (observer) {
            kendo.bind($(winId), observer);
            $(winId).data("viewModel", observer);
        }
        win.data("kendoWindow").open().center();
        win.parents("div.k-window").css("-moz-transform", "");
    };

    m.closeEditDialogWin = function(winId){
        $(winId).data("kendoWindow").close();
    };
    
    
	m.mapFields=function(el){
		var fields = {};
		$(el).find(":text,input[type=hidden],input[type=password],select,textarea,:radio:checked").each(function(){
			var key = $(this).attr("name");
			var val = $.trim($(this).val());
			fields[key]=val;
		})
		
		return fields;
	}   
	
	
	m.setAreaSelect=function(){
        $("select[name=province]").html('<option value="">所有</option>');
        $("select[name=city]").html('<option value="">请选择...</option>');
        for(var p in  window.nb_areas){
            $("select[name=province]").append("<option value='"+p+"'>"+p+"</option>");
        }
        $("select[name=province]").bind("change",function(){
            var pro = $(this).val();
            city_list = window.nb_areas[pro];
            $("select[name=city]").html('<option value="">请选择...</option>');
            for (var index in city_list){
                $("select[name=city]").append("<option value='"+city_list[index]+"'>"+city_list[index]+"</option>");
            }
        })
    };
    
    
    
})(jQuery);