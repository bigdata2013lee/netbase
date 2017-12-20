//技术领域字典对象定义
window.technologyFileds={
    //"操作系统"
    "操作系统":[
        {label:"操作系统", icon:"default.jpg"},
        {label:"Unix", icon:"default.jpg"},
        {label:"FreeBSD", icon:"default.jpg"},
        {label:"Solaris", icon:"default.jpg"},
        {label:"AIX", icon:"default.jpg"},
        {label:"HP-UX", icon:"default.jpg"},
        {label:"IRIX", icon:"default.jpg"},
        {label:"Tru64", icon:"default.jpg"},
        {label:"MS-DOS", icon:"default.jpg"},
        {label:"Linux", icon:"default.jpg"},
        {label:"Mac OS", icon:"default.jpg"},
        {label:"Windows", icon:"default.jpg"},
        {label:"Windows NT", icon:"default.jpg"}
    ],
    //"数据库"
    "数据库":[
        {label:"数据库", icon:"default.jpg"},
        {label:"MySQL", icon:"default.jpg"},
        {label:"PostgreSQL", icon:"default.jpg"},
        {label:"Microsoft Access", icon:"default.jpg"},
        {label:"SQL Server", icon:"default.jpg"},
        {label:"FileMaker", icon:"default.jpg"},
        {label:"Oracle", icon:"default.jpg"},
        {label:"Sybase", icon:"default.jpg"},
        {label:"dBASE", icon:"default.jpg"},
        {label:"Clipper", icon:"default.jpg"},
        {label:"FoxPro", icon:"default.jpg"},
        {label:"BigTable", icon:"default.jpg"},
        {label:"Cassandra", icon:"default.jpg"},
        {label:"MongoDB", icon:"default.jpg"},
        {label:"CouchDB", icon:"default.jpg"},
        {label:"Apache Cassandra", icon:"default.jpg"},
        {label:"Dynamo", icon:"default.jpg"},
        {label:"LevelDB", icon:"default.jpg"}
    ],
    //"网络与安全"
    "网络与安全":[
        {label:"网络与安全", icon:"default.jpg"},
        {label:"中继器", icon:"default.jpg"},
        {label:"网桥", icon:"default.jpg"},
        {label:"路由器", icon:"default.jpg"},
        {label:"网关", icon:"default.jpg"},
        {label:"防火墙", icon:"default.jpg"},
        {label:"交换机", icon:"default.jpg"}
    ],
    
    //"中间件"
    "中间件":[
        {label:"中间件", icon:"default.jpg"},
        {label:"apache", icon:"default.jpg"},
        {label:"nginx", icon:"default.jpg"},
        {label:"tomcat", icon:"default.jpg"},
        {label:"weblogic", icon:"default.jpg"},
        {label:"jboss", icon:"default.jpg"}
    ],
    //编程语言
    "编程语言":[
    
        {label:"编程语言", icon:"default.jpg"},
        {label:"C", icon:"default.jpg"},
        {label:"Java", icon:"default.jpg"},
        {label:"Objective-C", icon:"default.jpg"},
        {label:"C++", icon:"default.jpg"},
        {label:"C#", icon:"default.jpg"},
        {label:"(Visual) Basic", icon:"default.jpg"},
        {label:"PHP", icon:"default.jpg"},
        {label:"Python", icon:"default.jpg"},
        {label:"JavaScript", icon:"default.jpg"},
        {label:"Visual Basic .NET", icon:"default.jpg"},
        {label:"Transact-SQL", icon:"default.jpg"},
        {label:"Perl", icon:"default.jpg"},
        {label:"Rubly", icon:"default.jpg"},
        {label:"ActionScript", icon:"default.jpg"},
        {label:"F#", icon:"default.jpg"},
        {label:"Lisp", icon:"default.jpg"},
        {label:"Pascal", icon:"default.jpg"}
    ]
};
//技术领域全局变量的定义
window.technologyFiledsSearch = function(text, existLabes){
    var inArray = function(text, list){
        for(var j = 0; j < list.length; j++){
            if(text==list[j])return true;
        }
        return false;
    }
    
    var _fileds = {}
    for(pLabel in window.technologyFileds){
        for(var i=0; i < window.technologyFileds[pLabel].length; i++){
            var item = window.technologyFileds[pLabel][i];
            if(inArray(item.label, existLabes)){continue;}
            if(item.label.toLowerCase().search(text.toLowerCase())>=0){
                if(!_fileds[pLabel]){_fileds[pLabel] = [];}
                _fileds[pLabel].push(item);
            }
        }
    }
    return _fileds;
}
