(function($){
    
    var _validateeditDialog=function(params){       
        var em = $("#form1 div.validateErrorMsg");
        var rules = {
            context:function(val){return val.replace(/\s/ig,'').split("<p></p>").join("").length<=1000 && val.replace(/\s/ig,'').split("<p></p>").join("").length >0}
        };
        var messages = {
            context:"请输入1000字以内的内容"
        };
        var validator = new nb.xutils.Validator(em, rules, messages);
        return validator.validate(params);            
    };
        
    var _validateFile = function(params){    	
        var em = $("#form1 div.validateErrorMsg");
        var rules = {
        	fileName:function(fileName){
	            var fileType = fileName.substring(fileName.lastIndexOf(".")+1,fileName.length).toLowerCase();
	    		var fileList=["txt","rar","zip","gz","tar","bz","gzip2","ppt","pptx","doc","docx","xlsx","xls", "wps","dps","et",
		                  "jpg","jpeg","psd","swf","png","raw","bmp","tiff","svg","gif"]
		        if($.inArray(fileType,fileList) < 0 ){return false}
		        return true
        	},
        	fileSize:function(fileSize){return fileSize/1024/1024 <=10}
        };
    	var messages ={
    		fileName:"您的文件格式无法上传",
    		fileSize:"您上传的文件不能超过10M"
    	};
        var validator = new nb.xutils.Validator(em, rules, messages);
        return validator.validate(params);       
    }

	

    $(document).ready(function(){
  
	    $("#form1 dl dd input[name=Filedata]").bind("change",function(){
			var file = $("#form1 dl dd input[name=Filedata]").get(0).files[0];
			var params = {};
			params.fileName = file.name;		
			params.fileSize = file.size;
            if(!_validateFile(params)){$("#form1 dl dd input[name=Filedata]").val("");return false}; 			
		})

        $("#editor").kendoEditor();
        $("#form1").bind("submit",function(){
            var context = $("#editor").data("kendoEditor").value();
            if(!_validateeditDialog({context:context})){return false};
            $("#hidden_context").val(context); 
        })

    });
})(jQuery);
