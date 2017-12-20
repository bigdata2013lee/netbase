(function($){
    var m = window.serviceNote = new nb.xutils.Observer();
    m.serviceNoteDialogsWidget = nb.BaseWidgets.extend("BaseListWidget", {
        _panel_id: "#serviceNoteDialogsWidget",
        _snUid:null,
        __pageSize: 5,
        remoteView:nb.rpc.serviceNoteViews,
        remoteMethod:"getDialogs",
        getRemoteParams:function(){return {snUid:this._snUid};},
        onLoad: function(){
            var self = this;
            $(self._panel_id).show();
        },
        addDialog:function(){
            var self = this;
            var content = $("#editor").data("kendoEditor").value();
            var params = {snUid:self._snUid, content:content}
            nb.rpc.serviceNoteViews.c("addDialog", params)
            .success(function(msg){
                self.reload();
                $("#editor").data("kendoEditor").value("")
            });
        },
        
        displayEditor:function(fg){
            var self = this;
            if(fg){
                $(self._panel_id + " .send_msg_box").show();  
            }
            else{
                $(self._panel_id + " .send_msg_box").hide();  
            }
          
        },

        __init__: function(){
            var self = this;
            $(self._panel_id).hide();
            var tools = [
                "formatting",
                "bold",
                "italic",
                "underline",
                "justifyLeft",
                "justifyCenter",
                "justifyRight",
                "justifyFull",
                "insertUnorderedList",
                "insertOrderedList",
                "indent",
                "outdent",
                "createLink",
                "insertImage",
                "foreColor"
                ];
            $("#editor").kendoEditor({tools: tools, messages:xKendoMessages.editor});
            $(self._panel_id + " button[name=send_btn]").bind("click", function(){
                nb.xutils.delayTask("sendText", function(){ self.addDialog(); }, 1000);
            });
            
        }
    });
    
    
    
    m.attachmentsWidget={
        _panel_id:"#attachmentsWidget",
        _snUid:null,
        _render:function(){
            
        },
        
        reload:function(){
            var self = this;
            var attachmentsEl = $(self._panel_id + " .attachments:first").html("");
            nb.rpc.serviceNoteViews.c("getAttachments", {snUid: self._snUid}).
            success(function(attachs){
                $.each(attachs, function(i, item){
                    var exp = /^[0-9a-f]+_/;
                    var fileName = item.replace(exp, "");
                    attachmentsEl.append($(nb.xutils.formatStr('<a href="/downloads/{0}">{1}</a>', item, fileName)));
                });
            });
        },
        
        displayUploadForm:function(fg){
            var self = this;
            if(fg){
                $("#attachment-form").show(); 
                $(self._panel_id + " a[name=upload]").show();
            }
            else{
                $("#attachment-form").hide(); 
                $(self._panel_id + " a[name=upload]").hide();
            }
          
        },
        __init__:function(){
            var self = this;
            $('#attachment-form').uploadify({
                'formData' : {},
                "auto": false,
                'height': 24,
                'buttonText' : '浏览文件...',
                'fileSizeLimit' : '5MB',
                'queueSizeLimit' : 1,
                'swf': '/media/ui/uploadify/uploadify.swf',
                'uploader' : '/remote/ServiceNoteApi/addAttachment/',
                onUploadSuccess:function(a,b){
                    self.reload();
                }
            });
            
            $(self._panel_id + " a[name=upload]").bind("click", function(){
                $('#attachment-form').uploadify("settings", "formData", {snUid:self._snUid})
                $('#attachment-form').uploadify('upload');
            });
        }
    };
    
    
    
    
    $(document).ready(function(){
       m.serviceNoteDialogsWidget.__init__();
       m.attachmentsWidget.__init__();
    });
    
    
    
    
    
})(jQuery);
