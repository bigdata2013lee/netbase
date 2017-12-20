(function(){
    var $ = jQuery;
    var m = Ncm.utils = {
    
    
        connection2 : function(obj1, obj2){
            var conn =  null;
            var fillWidth = 3;
            if(obj1.from && obj1.to && obj1.line){
                conn = obj1; obj1 = conn.from; obj2 = conn.to;
            }
            var bb1 = obj1.boxRect.getBBox(), bb2 = obj2.boxRect.getBBox();
            var ps = [
                {x: bb1.x + bb1.width / 2, y: bb1.y + bb1.height / 2},
                {x: bb2.x + bb2.width / 2, y: bb2.y + bb2.height / 2}
            ];
            
            var ap = Math.pow(ps[0].x-ps[1].x,2) + Math.pow(ps[0].y-ps[1].y,2);
            var len = Math.sqrt(ap);
            
            var pathStr = Raphael.format("M {0} {1} l{2} {3} l {4} {5} l{6} {7}z", 
                ps[0].x, ps[0].y, len, 0, 0, fillWidth, -len, 0);
            
            //角度
            var jd = Math.atan2(ps[0].y - ps[1].y , ps[0].x - ps[1].x) * 180 / Math.PI + 180;
            //console.info(jd); 
            //jd = 0;   
                
            if(!conn){
                var line = Ncm.core.paper.path(pathStr);
                line.attr({'stroke-width': 0, fill: '#000'});
                line.rotate(jd, ps[0].x, ps[0].y);
                line.insertBefore(Ncm.core.__firstFgPath);
                return {from: obj1, to: obj2, line: line};
            }else{
                conn.line.attr({'path': pathStr, transform:''});
                conn.line.rotate(jd, ps[0].x, ps[0].y);
                return conn;
            }
            return conn ;
        },
    

        /** 获取事件在页面中的坐标 */
        getPageXY: function(evt){
            
            var scroll = {left:$(document).scrollLeft(), top: $(document).scrollTop()};
            //var offset = $("#canvas_continer").offset();
            var rs = {x:evt.clientX+scroll.left, y:evt.clientY+scroll.top};
            //console.info(evt);
            return rs;
        },
        
        /** 获取事件在画布中的坐标 */
        getMousePoint:function(evt){
            var offset = $("#canvas_continer").offset();//This is JQuery function
            var scroll = {left: $(document).scrollLeft(), top: $(document).scrollTop()};
            //console.dir(scroll);
            var x = evt.clientX - offset.left + scroll.left;
            var y = evt.clientY - offset.top  + scroll.top;
            //console.info(evt.pageY, evt.clientY, evt)
            return {x:x, y:y};
        },
        
        /** 画布中的坐标转换为页面坐标*/
        mousePoint2pagePoint:function(evt){
            var offset = $("#canvas_continer").offset();//This is JQuery function
            var scroll = {left: $(document).scrollLeft(), top: $(document).scrollTop()};
            var x = evt.clientX + offset.left - scroll.left;
            var y = evt.clientY + offset.top  -  scroll.top;
            return {x:x, y:y};
        }    
    
    
    };
    
    
    
    


    //延时任务管理功能
    m.DelayTaskMrg = {
        _tasks: {},
        _DelayTask : function(xfun){
            //console.info('new _DelayTask...');
            this.time = 1000;
            /** 执行 */
            this.excute = function(){ xfun(arguments); };
            
            /** 
             * 运行, 在time毫秒内再次执行此任务，上次未执行任务将被取消
             * @note 处理函数参数在time参数后面加入
             * @param {int} time
             */
            this.run = function(time){
                this.time = time;
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
    
       
    /** 计算流量级别　*/
    m.rateLevel = function(n){//计算级别未知为0， 
        if(!n) n = 0;
        n = n * 1;
        if(n>0 && n < 0.01) return 1;
        if(n>=0.01 && n < 10) return 2;
        if(n>=10 && n < 60) return 3;
        if(n>=60 && n < 80) return 4;
        if(n>=80) return 5;
        if(n<= 0) return 0;
        
        return  0
        
    };
    
    /**　创建生成流量滤镜　*/
    m._createFlowGradient = function(finLevel, foutLevel, tinLevel, toutLevel){
        //灰紫蓝绿橙红黑0123456
        var colors = ['#A09D9D', '#AD0DDD', '#061CE0', '#069612', '#F4A004', '#DB1904','#000000'];
        
        //Raphael.format
        var p = "0-{0}:0-{0}:24-{1}:26-{1}:49-{2}:51-{2}:74-{3}:76-{3}:100";
        var g = Raphael.format(p, colors[finLevel], colors[foutLevel], colors[toutLevel], colors[tinLevel]);
        return g;
        
    };
    
    m.fillLineGradient=function(conn, from_flowInfo, to_flowInfo){
        var finLevel = 6, foutLevel = 6, tinLevel = 6, toutLevel = 6;
        
        finLevel = m.rateLevel(from_flowInfo ? from_flowInfo.inputRate:-1);
        foutLevel = m.rateLevel(from_flowInfo ? from_flowInfo.outputRate : -1);
    
        tinLevel = m.rateLevel(to_flowInfo ? to_flowInfo.inputRate : -1);
        toutLevel = m.rateLevel(to_flowInfo ? to_flowInfo.outputRate : -1);
        
        var g = m._createFlowGradient(finLevel, foutLevel, tinLevel, toutLevel);
        
        if(Ncm.core.paper.raphael.svg){
            var oTransform = conn.line.attr('transform');
            conn.line.attr({'transform': ''});
            conn.line.attr({'fill': g});
            conn.line.attr({'transform': oTransform});
        }
        else{
            conn.line.attr({'fill': g});
        }
    
    };
    
		/**
		 * 把一个值转为2位小数
		 * 如果非数字，返回原值，带单位的情况，返回值+单位
		 * @param {Object} val
		 * @param {string} u 单位
		 */
		m.toNum2 = function(val, u, rate, nullStr) {
		    nullStr = nullStr ? nullStr : "N/A";
		    rate = rate ? rate : 1;
			if (val === "" || val === null || val == undefined){
			    if(u) return nullStr;
				else{return null;}
			}
			if (isNaN(val * 1)) {
				return val;
			}
			if ( typeof val === "boolean") return val;
			
			
			val = val * rate;
	
			var exp = /^(\d+)(\.\d{0,2})?\d*$/;
			exp.test(val + "")
			var _val = RegExp.$1 + RegExp.$2;
			_val = _val * 1;
			if (u)
				return _val + "" + u;
			return _val
		}
		
		
	m.byte2readable = function(val, bps, k, nullStr){
	    if(!nullStr) nullStr = "";
	    var _val = parseFloat(val);
	    if(isNaN(_val)) return nullStr;
	    if(! k) k = 1024;
	    var keys = [{name:"G", val: k*k*k},{name:"M", val: k*k}, {name:"K", val: k}, {name:"B", val: 1}];
	    if(bps){
	        keys = [{name:"Gbps", val: k*k*k},{name:"Mbps", val: k*k}, {name:"Kbps", val: k}, {name:"bps", val: 1}];
	    }
	    for(var i=0; i < keys.length; i++){
	        if(_val >= keys[i].val){
	            var x =  _val/keys[i].val;
	            return this.toNum2(x, keys[i].name);
	        }
	    }
	    
	    return _val;
	}

})();