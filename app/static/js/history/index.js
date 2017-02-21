String.prototype.replaceAll = function (exp, newStr) {
    return this.replace(new RegExp(exp, "gm"), newStr);
};

/**
 * 原型：字符串格式化
 * @param args 格式化参数值
 */
String.prototype.format = function(args) {
    var result = this;
    if (arguments.length < 1) {
        return result;
    }

    var data = arguments; // 如果模板参数是数组
    if (arguments.length == 1 && typeof (args) == "object") {
        // 如果模板参数是对象
        data = args;
    }
    for ( var key in data) {
        var value = data[key];
        if (undefined != value) {
            result = result.replaceAll("\\{" + key + "\\}", value);
        }
    }
    return result;
}

var Data;
var page=1;
var one_page=1000;
var total_page=1;
var csrftoken=$('meta[name=csrf-token]').attr('content');

function get_data(){
   $.ajax({
     url:"/History/get_data/{page}/{one_page}".format({page:page, one_page:one_page}),
     type:"GET",
     data:{csrftoken:csrftoken},
     beforeSend:function(XMLHttpRequest){
       console.log("beforeSend");
     },
     error:function(XMLHttpRequest, textStatus, errorThrown){
        console.log('error')
     },
     success:function(data){
       console.log(data);
     }
   });
}
