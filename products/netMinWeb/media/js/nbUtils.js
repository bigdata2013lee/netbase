(function($){
    
    var consoleEnable = true; //是否启用控制台,在布置时设置为false
    if(!consoleEnable){
        if(!window.console){window.console = {};}
        console.info = function(){};
        console.log = function(){};
        console.debug = function(){};
        console.warn = function(){};
        console.error = function(){};
    }
    
    

    
    
    
    //----------------命名空间初始化--------------------------
    window.nb = {};

    nb.nameSpace = function(ns) {
        var a = arguments, o = nb;
        var x = ns.split('.');
        for (var i = 0; i < x.length; i++) {
            o[x[i]] ? "" : o[x[i]] = {};
            o = o[x[i]];
        }
        return o;

    };

    /**
     * 创建、原型继承类
     * @param supper: 父类, 可选参数
     * @param props: 属性及方法
     * var Person  = nb.Class(super, {
     *     __init__: function(name){ this.name = name;}
     *     sayHello: function(){console.info("Hello everyone. I am %s", this.name)}
     * }) 
     */
    nb.Class = function(){
        if(arguments.length == 0){
            throw new Error("Argument error! Create new class, please writting as: Class([super], {...})");
        }
        var superCls = arguments.length == 2 ?  arguments[0] : function(){};
        var newCls = function(){
            this.__super__ = superCls;
            if(this.__init__) this.__init__.apply(this, arguments);
        };
        var pros = arguments.length == 1 ? arguments[0] :arguments[1];
        
        for(var key in superCls.prototype){
            newCls.prototype[key] = superCls.prototype[key];
        }
        
        for(var key in pros){
            newCls.prototype[key] = pros[key];
        }
        
        return newCls;
    };
    
    //-------------------------------------------------------------------------------//
    var xutils = nb.xutils = {};
    
    

    /**
     * 格式化字符串
     * 示例代码:
     * formatStr('Hello {0}, I klie {1}','word', 'JS');
     * >>>Hello word, I klie JS
     */
    xutils.formatStr = function() {
        var str = arguments[0];
        for (var i = 1; i < arguments.length; i++) {
            var reg = eval("(/\\{\\s*" + (i - 1) + "\\s*\\}/gi)");
            str = str.replace(reg, arguments[i]);
        }
        return str;
    }
    
    xutils.showMoney = function(money){
        return "￥" + money.toFixed(2);
    }
    
    xutils.ReDecimalPoint = function(num, pointNum){
        var x = num*1;
        return x.toFixed(pointNum);
    }
    
    
    //取得查询条件
    xutils.setQueryConditions = function(id, flag) {
        
        var letters = {
                "\\\\" : /\\/,
                "\\." : /\./g,
                "\\+" : /\+/g,
                "\\*" : /\*/g,
                "\\?" : /\?/g,
                "\\-" : /\-/g
           };
        var conditions = {};
        $(id + " input").each(function(){
            var condition = $(this).val();
            var attrName = $(this).attr("name")
            if (condition && $.trim(condition) != "") {
                conditions[attrName] =  condition;
                //$.each(letters, function(key, val){
                    //condition = condition.replace(val, key);
                    //conditions[attrName] = "regex:" + condition;
                   
              //  });
            }
        });
        if(flag){
             var selectBt = $( id + " select").val();
            if (selectBt != 4) {
                conditions["status"] = selectBt;
            }
        }
        
        return conditions;
    };
    
    
    
    xutils.formStatusD2C = function(status){
        var formStates ={0: "未审核", 1:"通过",  2:"不通过"}
        return formStates[status]
    }
    
    
    xutils.isEmpty = function(value){
        if(! value) return true;
        
        if(typeof(value) == "function"){ return false;}
        if(typeof(value) == 'string'){
            if($.trim(value) == '') {return true;}
            return false;
        }
        
        if(typeof(value)=="object" && value.reverse){ //list
            if(value.length == 0) return true;
            return false;
        }
        
        var findKey = false;
        for(var key in value ){ //comon object
            findKey= key;
            break;
        }
        if(findKey == false) return true;
        
        return false;
    }
    
    /**
     * 替换正则中的特殊字符 
     */
    xutils.replaceXletters = function(str){
        var letters = { "\\\\" : /\\/, "\\." : /\./g, "\\+" : /\+/g, "\\*" : /\*/g, "\\?" : /\?/g, "\\-" : /\-/g }; //用于替换正则中的特殊字符
        $.each(letters, function(key, val) {
                str = str.replace(val, key);
        })
        return str;
    };



    xutils.getTimeStr  = function(time, sortFormat){
        var fm = "{0}-{1}-{2} {3}:{4}";
        if(sortFormat){fm = "{0}-{1}-{2}";}
        var fix0 = function(n){
            if(n < 10) return "0" + n;
            return n + "";
        };
        if(time == 0) return "";
        if(time *1 == NaN) return '';
        var d = new Date();
        d.setTime(time*1);
        return xutils.formatStr(fm, d.getFullYear(), 
                    fix0(d.getMonth()+1), fix0(d.getDate()), fix0(d.getHours()), fix0(d.getMinutes()))
    };
    
    xutils.formatDate = function(time){
    	
    }
    
    xutils.verboseTrueFalse = function(val){
        if(val){return "是";}
        return "否";  
    };
    
    xutils.val2boolean = function(val){
        if(val == "是" || val == "yes" || val == "true") return true;
        if(val == "否" || val == "no" || val == "false") return false;
        
        if(val) return true;
        return false;
    }
    
    xutils.val2booleanStr = function(val){
        if(val == "是" || val == "yes" || val == "true") return true + "";
        if(val == "否" || val == "no" || val == "false") return false +"";
        if(val) return true + "";
        return false + "";
    }
    
    /**
     * 删除对象属性
     * simple: delattrs(obj, "name", "age", ...) 
     */
    xutils.delattrs = function(){
        if(arguments.length < 2) return;
        var obj = arguments[0]
        if(! obj ) return;
        
        for(var i=1, len= arguments.length; i<len; i++){
            delete obj[arguments[i]];
        }
    }
    
    xutils.Observer = function(){
        this.events = {};
        
        /** 触发事件  */
        this.fireEvent = function(eName){
            var events = this.events[eName];
            if(! events) return;

            var handlerArguments = [];
            for(var i = 1; i < arguments.length; i++){
                handlerArguments.push(arguments[i]);
            }

            for(var i = 0; i < events.length; i++){
                var event = events[i];
                event.handler.apply(event.scope || this, handlerArguments);
            }

        };
        
        /** 事件绑定 */
        this.on = function(eName, handler, scope){
            if(!this.events[eName])  this.events[eName] = [];
            this.events[eName].push({handler: handler, scope: scope});
        };

        /** 取消事件，如果handler不存在，取消所有事件 */
        this.un = function(eName, handler){
            var events = this.events[eName];
            if(!events || events.length == 0) return;
            if(events && !handler){
                events.splice(0, events.length);
                return;
            }
            

            for(var i = events.length - 1; i >= 0; i--){
                if(events[i].handler == handler) events.splice(i,1);
            }
        }
    };
    


    //延时任务管理功能
    xutils.DelayTaskMrg = {
        _tasks: {},
        _DelayTask : function(xfun){
            //console.info('new _DelayTask...');
            this.time = 800;
            /** 执行 */
            this.excute = function(){ xfun(arguments); };

            /** 
             * 运行, 在time毫秒内再次执行此任务，上次未执行任务将被取消
             * @note 处理函数参数在time参数后面加入
             * @param {int} time
             */
            this.run = function(time){
                if(time){
                    this.time = time;
                }
                clearTimeout(this._taskTimer);
                var newArguments = [];
                for(var i = 1; i < arguments.length; i++){
                    newArguments.push(arguments[i]);
                }
                this._taskTimer = setTimeout(function(){xfun.apply({},newArguments)}, this.time);
            }

        },
        /**
         * 创建延时任务
         * @param {String} id 唯一任务ID，如果id已经存在，则返回已创建的任务对象
         * ＠param {Function} xfun 任务处理函数
         */
        createTask: function(id, xfun){
            if(this._tasks[id]) return this._tasks[id];
            var task = new this._DelayTask(xfun);
            this._tasks[id] = task;
            return task;
        }
    };
    
    xutils.delayTask = function(tid, xfun, time){
        xutils.DelayTaskMrg.createTask(tid, xfun).run(time);
    }


    //------------------------------------------------------------------------------------------//
    
    xutils.isValidIp = function(ip){
        if(ip == "255.255.255.255")return false;
        if(/^0{1,3}\.0{1,3}\.0{1,3}\.0{1,3}$/.test(ip)) return false;
        
        var exp = /^(?:(?:[1-9]?[0-9]|1[0-9]{2}|2(?:[0-4][0-9]|5[0-5]))\.){3}(?:[1-9]?[0-9]|1[0-9]{2}|2(?:[0-4][0-9]|5[0-5]))$/;
        if(exp.test(ip)){return true}
        return false
        
        
    };
    
    xutils.isValidUrl = function(ip){
        var exp = /^[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?$/;
        if(exp.test(ip)){return true}
        return false
    };
    
    xutils.isValidMac = function(ip){
        var exp = /^\s*([0-9a-fA-F]{2,2}[:|-]){5,5}[0-9a-fA-F]{2,2}\s*$/;
        if(exp.test(ip)){return true}
        return false
    };

    
    
    xutils.isVaildEmail = function(email){
        var exp = /^[0-9a-zA-Z_\.#]+@(([0-9a-zA-Z]+)[.])+[a-z]{2,4}$/;
        if(exp.test(email)){return true}
        return false
    };
    
    xutils.isVaildPhone = function(phone){
        var exp1 = /^0\d{2,3}-\d{7,8}$/;
        var exp2 = /^1\d{10,10}$/;
        
        if(exp1.test(phone) || exp2.test(phone)){return true;}
        return false;
    }

    
    xutils.isValidNum = function(val){
        var exp = /^-?\d+(\.\d+)?$/;
        if(exp.test(val)){
            return true
        }
        return false
    },  


    /**
     * trim 对象属性的空格，只对字符类型的属性有效
     * @param {Object} obj
     * @param {Object} pns 可选参数，属性名列表
     */
    xutils.trimObj = function(obj, pns){
        $.each(obj, function(key, value){
            if(typeof value !== 'string') return;
            if(!pns || pns.length == 0){
                obj[key] = $.trim(value);
            }
            else if($.inArray(key, pns) >= 0){
                obj[key] = $.trim(value);
            }
        });    
    };
    
    //------------------------------------------------------------------------------------------------/
    
   window.importCss=function(url){
   		var head = $("head:first");
   		if(head.find('link[href="'+url+'"]').size() == 0){
	        var link = $('<link rel="stylesheet" type="text/css" href="'+url+'"/>');
	        $("head:first").append(link);
   		}
    };

    //----------------------------------------------------------------------------------------//
    
   


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
})(jQuery);
