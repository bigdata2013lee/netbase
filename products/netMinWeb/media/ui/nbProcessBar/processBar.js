
/**
 * 
 * @param {Object} val
 * @param {Object} rate 1 或者 100
 */
var nbProcessBar = function(val, rate, dir){
    this.val = val;
    _rate = rate ? rate : 100;
    var _tpl ='<span class="process_bar {1}"> \
            <div class="inner"><div class="p"  style="width:{0}%;"></div></div> \
            <div class="text">{0}%</div><br clear="both"/> \
        </span>';
        
    var _NaNtpl ='<span class="process_bar"> \
            <div class="inner"><div class="p"></div></div> \
            <div class="text">NAN</div><br clear="both"/> \
        </span>';
    
    this._level = function(val){
        if(dir=='down'){
            if(val >=0 && val < 25) return "aa";
            else if( val >=25  && val < 50) return "bb";
            else if( val >=50  && val < 75) return "cc";
            else if( val >=75) return "dd";
            return "";
        }
        
        
        if(val >=0 && val < 25) return "dd";
        else if( val >=25  && val < 50) return "cc";
        else if( val >=50  && val < 75) return "bb";
        else if( val >=75) return "aa";
        return "";
    }
    this.html=function(){
        var exp = /^(\d+)(?:(\.\d)\d+)?$/;
        if(exp.test(val)){
            var _val = (RegExp.$1 + RegExp.$2)*_rate;
            if(_val > 100){_val = 100}
            var level = this._level(_val);
            return nb.xutils.formatStr(_tpl, _val, level);
        }
        return nb.xutils.formatStr(_NaNtpl);
    };
    
    this.appenTo = function(el){
        $(el).append(this.html());
    }
    
}
