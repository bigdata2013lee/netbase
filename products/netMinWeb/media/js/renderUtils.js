(function($){
		
	var ns = nb.nameSpace("Render");
	$.extend(ns,{
	   
	    checkEnable:function(startUpIPMI){
	        
	        if(startUpIPMI == true){
	            return '<a  href="javascript:" id="checkEnableBootpo">关闭</a>';
	        }else if(startUpIPMI == false){
	            return '<a  href="javascript:" id="checkEnableBootpo">启动</a>';
	        }else{
	            return "N/A";
	        }
	        
	    },
	    
	    formatTime:function(timeStamp){
	        
	        t = new Date(timeStamp*1000);
	        return t.toLocaleString();
	    },
	    
	    IisTotalUsers:function(nonUser, user){
	        return nonUser+"/"+user;
	    },
	    
	    IisFileRS:function(r, s){
	        return r+"/"+s;
	    },
	    
	    Kb2Mb : function(val){
	        return (val/(1024*1024)).toFixed(2)+" MB";
	    },
	    
	    JvmUsed: function(used, max){
	        
	       return (used/(1024*1024)).toFixed(2)+" MB" + " ( "+(100*used/max).toFixed(0)+"% )";
	    },
	    
	    busyAndIdle: function(busy, idle){
	        
	        return busy + "/" + idle;
	    },
	    
	    nginxServerACR:function(a,c, r){
	        
	        return a +"/"+c+"/"+r;
	    },
	    
	    nginxRWW: function(reading, writing, waiting){
	        
	        return reading +"/"+writing+"/"+waiting;
	    },
	    
		severitys : function(sev) {
			var _severitys = { 5 : "Critial", 4 : "Error", 3 : "Warning", 2 : "Debug", 1 : "Info", 0 : "Clear" };
			return _severitys[sev];
		},
	    severitys2zh : function(sev) {
	        var _severitys = { 5 : "严重", 4 : "错误", 3 : "警告", 2 : "调试", 1 : "信息", 0 : "恢复" };
	        return _severitys[sev];
	    },
		byte2readable:function(val, bps, k, nullStr){
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
		},
	    serviceNoteStatus: function(val){
	        var status = {0:"处理中",1:"待审中",2:"结束"};
	        return status[val];
	    },
	
		percent : function(val, u, rate) {
		    if(!rate) rate = 100;
			if (val === null || val == undefined){
			    if(u) return "N/A";
	            else{return null;}
			}
			if (isNaN(val * 1)) {
				return val;
			}
			if ( typeof val === "boolean")
				return val;
			val = val * rate;
			//console.info(val);
			var exp = /^(\d+)(\.\d{0,1})?\d*$/;
			exp.test(val + "")
			var _val = RegExp.$1 + RegExp.$2;
			if(u) return _val + "" + u;
			return _val * 1;
		},
	
		/**
		 * 把一个值转为2位小数
		 * 如果非数字，返回原值，带单位的情况，返回值+单位
		 * @param {Object} val
		 * @param {string} u 单位
		 */
		toNum2 : function(val, u, rate, nullStr) {
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
		},
		
		deviceEventLabel: function(title, componentType, deviceIp){
		    var max = 28;
		    var componentTypes = {"Network":"网络设备", "Device":"设备", "IpService":"IP服务", "Process":"进程", "IpInterface":"接口", "FileSystem":"文件系统"};
		    var label = "";
		    if(componentType == "Device" || componentType == "Network"){
		        label =  componentTypes[componentType] + ":" + title;
		    }
		    else if(deviceIp){
	    	    label = "设备:" + deviceIp + " " + (componentTypes[componentType] || componentType) + ":" + title;
		    }
		    else{
		        label = componentTypes[componentType] + ":" + title;
		    }
		    
		    return label;
		},
		
	    monitorObjName :function(monitorObjName){
	        var exp = /^([a-zA-Z]+)(_)(.+)$/;
	        if(exp.test(monitorObjName)){
	            var componentType = RegExp.$1;
	            var moTitle = RegExp.$3;
	            return this.zh(componentType) + ":" + moTitle;
	        }
	        return monitorObjName;
	    },
		
		userGroup:function(group){
		  var groups = {idc:"IDC用户",comm:"普通用户", enterprise :"企业用户"};
		  return groups[group] || ""  
		},
		/**
		 * 截取一定长度的字符，并补省略号
	     * @param {Object} str
	     * @param {Object} max
		 */
		ellipsisStr: function(text, length, position){
		    length ? "" : length = 28;
		    position ? "" : position="center"
		    if(text != null && text.length <= length){return text}
	        if(position == "right"){return text.substr(length) + "..."} 
	        
	        if(text != null && position != "right"){
	            var lenL = length / 2;
	            var lenR = length - lenL;
	            return text.substr(0,lenL) + "..."+ text.substr(text.length-lenR);
	        }
	        return text
	
		},
		

	    createCpuMemGauge:function(cpu,mem) {
	        var cpu_str = 'N/A';
	        var mem_str = 'N/A';
	        var status = "";
	        var html = '<div class="gauge_cpu"></div><div class="gauge_mem">\
	        </div><div class="gauge_cpu_value">N/A</div><div class="gauge_mem_value">N/A</div>';
	        var containerId = "#cpumem-gauge-container";
	        
	        $(containerId).removeClass("unknown");
	        $(containerId).html("").append($(html));
	        if(!$.isNumeric(cpu) && !$.isNumeric(mem)){
	            $(containerId).addClass("unknown");
	        }
	        
	        if($.isNumeric(cpu)){
	            cpu = Math.round(cpu*10)/10;
	            cpu_str = cpu + "%";
	        }
	        else{
	            cpu = 0;
	        }
	        if($.isNumeric(mem)){
	            mem = Math.round(mem*10)/10;
	            mem_str = mem + "%";
	        }
	        else{
	            mem = 0;
	        }

	        $(containerId + " div.gauge_cpu").kendoRadialGauge({
	
	            pointer: {value: cpu},
	
	            scale: {
	                minorUnit: 5,
	                startAngle: -40,
	                endAngle: 220,
	                max: 100,
	                labels:{visible:false},
	                majorTicks:{visible:false},
	                minorTicks:{visible:false}
	                
	            }
	        })
	        
	        $(containerId + " div.gauge_cpu_value").html(cpu_str);
	        
	        $(containerId + " div.gauge_mem").kendoRadialGauge({
	
	            pointer: {value: mem},
	
	            scale: {
	                minorUnit: 5,
	                startAngle: -40,
	                endAngle: 220,
	                max: 100,
	                labels:{visible:false},
	                majorTicks:{visible:false},
	                minorTicks:{visible:false}
	                
	            }
	        });
	        $(containerId + " div.gauge_mem_value").html(mem_str);
	    },
        
        
		/** 文字汉化 */
		zh:function(text, map){
		    map ? "" : map = this.zh_map;
		    if(text in map) return map[text];
		    return text;
		},
		zh_map:{
		    "User":"用户", "EngineerUser":"工程师", "true":"是","false":"否",
		    "Website":"站点","Device":"主机","Bootpo":"远程开机","Process":"进程","IpInterface":"接口",
		    "MwApache":"Apache服务器","MwTomcat":"Tomcat服务器","MwNginx":"Nginx服务器",
		    "IpService":"Ip服务","FileSystem":"磁盘","Network":"网络","ShortCutCmd":"远程命令","Network":"网络"
		}
	});
	
	
	ns.constants={
		zfsm001:"了解具体资费，及相关收费办法，请参阅 <a href='/help/help_center_kfsm.html' target='_blank'> &lt;&lt;Netbase 资费细则&gt;&gt; </a>。"
	};

})(jQuery)