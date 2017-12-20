(function($){
    
    
    /**
     *一个消息提示工具 
     */
    var AlertTip = nb.AlertTip = {
    	cookieName : "alertTipMessages",
        _autoGotUserMsg: true,
        _autoGotUserMsgRange: 10, //秒
        _panel_id: "#AlertTip",
        _timer:0,
        _dalyClear:function(el){
            var self = this;
            setTimeout(function(){
                el.slideUp(400, function(){$(this).remove()});
            }, 1000 * 5);
        },
        
        storeCookie:function(msg){
        	var self = this;
        	var messages = $.cookie(self.cookieName) || "[]";
        	messages = $.evalJSON(messages);
        	messages.push(msg);
        	$.cookie(self.cookieName, $.toJSON(messages), {path:"/"});
        },
        warn: function(msg){
            var self = this;
            var msgBox = $('<div class="msgBox warn"></div>').html(msg);
            msgBox.appendTo($(self._panel_id));
            msgBox.hide();
            msgBox.slideDown();
            self._dalyClear(msgBox);
        },
        
        info: function(msg){
            var self = this;
            var msgBox = $('<div class="msgBox info"></div>').html(msg);
            msgBox.appendTo($(self._panel_id));
            msgBox.hide();
            msgBox.slideDown();
            self._dalyClear(msgBox);
        },
        
        auto: function(msg){
            var self = this;
            if(nb.xutils.isEmpty(msg)) return;
            if(/^\s*\w*_*warn\:(.+)/gi.test(msg)){ self.warn(RegExp.$1); return; } 
            self.info(msg);
        },
        
        
        got: function(){
            var self = this;
            if(!nb.rpc.userMessageViews) return;
            var rm = nb.rpc.userMessageViews.c("got");
            rm.success(function(userMsg){
               if(! userMsg) return;
               if(userMsg.msgtype=="warn"){self.warn(userMsg.msg)}
               else if(userMsg.msgtype=="info"){self.info(userMsg.msg)}
            });
        },
        
        __init__:function(){
            var self = this;
            var html = '<div id="AlertTip"> </div>';
            var alertTipEl = $(html);
            alertTipEl.appendTo($(document.body));
            var autoGotUserMsgTimer = 0;
            
            $(document).ajaxError(function(evt,jqXHR, settings){
                if(settings.url == "/remote/UserMessageApi/got/"){return;}
                if(jqXHR.status!=500){return;}
                self.warn("连接服务器发生错误.") 
            });
            
            if($.cookie){ //在jquery cookie支持的情况下，加载页面时，显示提示信息
	            var messages = $.cookie(self.cookieName) || "[]";
	        	messages = $.evalJSON(messages);
	            $.each(messages, function(i, msg){ self.auto(msg); });
	            messages=[];
	            $.cookie(self.cookieName, $.toJSON(messages), {path:"/"});
            }
            
           
        }
        
    };
    
    
    
    $(document).ready(function(){
        
        AlertTip.__init__();
    });
    
    
})(jQuery);
