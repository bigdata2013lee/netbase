(function($){
    var rpc = nb.nameSpace("rpc");
    
    //---------------------------------------------------------------------------------//
    var remoteUrls = window.remoteUrls || [];
    
    for (var i = 0; i < remoteUrls.length; i++) {
        var viewName = remoteUrls[i]['viewName'];
        var remoteUrl = remoteUrls[i]['remoteUrl'];
        var createObj = function(viewName, remoteUrl) {
            rpc[viewName] = {};

            rpc[viewName].c = function(method, params, dataType, async) {
                if ( typeof params == 'undefined') params = {};
                if (!dataType) { dataType = "json";  }
                if(async !== false){async = true}
                
                var _params = $.toJSON( typeof params === "function" ? params() : params);
                var url = remoteUrl + method + '/';
                return $.ajax({
                    url : url,
                    type : "POST",
                    async : async,
                    data : {
                        params : _params
                    },
                    dataType : dataType
                });
            };

            rpc[viewName].rc = function(method, params) {
                if ( typeof params == 'undefined')
                    params = {};
                var url = remoteUrl + method + '/';
                var readConfig = {
                    url : url,
                    type : 'post',
                    dataType : "json",
                    data : {
                        params : typeof (params) == 'function' ? function() {
                            return $.toJSON(params())
                        } : $.toJSON(params)
                    }
                }

                return readConfig;
            };
            //end remoteRead fun

        };

        createObj(viewName, remoteUrl);
    }

    
    
    //----------------------------------------------------------------------------------//
    
    
})(jQuery);