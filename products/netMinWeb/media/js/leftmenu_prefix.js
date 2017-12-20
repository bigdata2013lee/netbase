(function($){
	$(document).ready(function(){
	    
       if(window.nb_secNav != undefined){
            $("#mleft-panel #left-menus li a:eq("+nb_secNav+")").addClass("selectedMenu");
            return;
        }
        
        menuList = $("#mleft-panel #left-menus li").find("a");
        pageUrl =window.location.pathname.replace(window.orgUid+"/","");
        for( i=0;i<menuList.length;i++){
            var hf = $(menuList[i]).attr("href");
            if(hf.indexOf("?")>=0){
                hf = $(menuList[i]).attr("href").substring(0,$(menuList[i]).attr("href").indexOf("?"))
            }
            if (hf  == pageUrl){
                $(menuList[i]).addClass("selectedMenu");
            }
        }


	});	
})(jQuery)
