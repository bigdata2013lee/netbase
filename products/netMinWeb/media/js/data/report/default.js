(function($){
    
    var m = window.Index = new nb.xutils.Observer();
    m.currentDevId = window.moUid;
   	
   	reportListTree.on("selectOrgNode",function(orgUid, uname){
        if(orgUid !== "0"){
        	window.location.href = "/report/content/"+orgUid;
       }
    });
    
})(jQuery);
