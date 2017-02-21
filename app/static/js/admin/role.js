
/**
 * 替换所有匹配exp的字符串为指定字符串
 * @param exp 被替换部分的正则
 * @param newStr 替换成的字符串
 */
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

String.prototype.Trim = function(){
  return this.replace(/(^\s*)|(\s*$)/g, "");
}

String.prototype.LTrim = function(){
  return this.replace(/(^\s*)/g, "");
}

String.prototype.RTrim = function(){
  return this.replace(/(\s*$)/g, "");
}

var role_data; // 存放role表的数据
var module_data; // 存放module表的数据

function hidden_role_form(){
  // 隐藏role表单
  var $wbox = $("#roleform");
  $wbox.hide(500);
}

function hidden_module_form(){
  // 隐藏module表单
  var $wbox = $("#moduleform");
  $wbox.hide(500);
}

function get_role(){ // 获取role表数据
  var a = $.ajax({
      url:"/admin/api/role",
      async:false,
      })
  role_data = a.responseJSON;
}

function get_module(){ // 获取module表数据
  var a = $.ajax({
      url:"/admin/api/module",
      async:false,
      })
  module_data = a.responseJSON;
}

function create_role_table(){ // 填充role表的数据
  $("#role tbody").empty();
  $.each(role_data.data, function(n, values){
      var tr_dom = $("<tr></tr>",{id:"role_{id}".format({id:values.id})});
      $("<td></td>",{text:values.id}).appendTo(tr_dom);
      $("<td></td>",{text:values.name}).appendTo(tr_dom);
      if (values.status==1){
        $("<td><span class='label label-success'>正常</span></td>").appendTo(tr_dom);
      }else if (values.status==0){
        $("<td><span class='label label-danger'>停用</span></td>").appendTo(tr_dom);
      }else{
        $("<td><span class='label label-danger'>非正常</span></td>").appendTo(tr_dom);
      }
      if (values.status==1){
          $("<td><button class='btn btn-xs btn-warning' onclick='edit_role({id})'><i class='icon-pencil'></i></button>\
          <button class='btn btn-xs btn-danger' onclick='change_role_status({id})'><i class='glyphicon glyphicon-stop'></i></button></td>".format({id:values.id})).appendTo(tr_dom);
      }else if (values.status==0){
        $("<td><button class='btn btn-xs btn-warning' onclick='edit_role({id})'><i class='icon-pencil'></i></button>\
          <button class='btn btn-xs btn-success' onclick='change_role_status({id})'><i class='glyphicon glyphicon-play'></i></button></td>".format({id:values.id})).appendTo(tr_dom);
      }
      tr_dom.appendTo("#role tbody");
  });
}

function change_role_status(id){ // 修改某一个role的状态
  $.ajax({
       url:"/admin/api/role/{id}".format({id:id}),
       async:false,
       type:"DELETE",
       // data:{uid:id},
       success:function(data){
                  if (data.status == 1){
                     if (data.role_status == 0){
                         $("#role_{id} td:eq(2) span".format({id:id})).attr({"class":"label label-danger"});
                         $("#role_{id} td:eq(2) span".format({id:id})).text("停用");
                         $("#role_{id} td:eq(3) button.btn-danger i[class='glyphicon glyphicon-stop']".format({id:id})).attr("class", "glyphicon glyphicon-play");
                         $("#role_{id} td:eq(3) button.btn-danger".format({id:id})).attr("class", "btn btn-xs btn-success");
                     }
                     else if (data.role_status == 1){
                         $("#role_{id} td:eq(2) span".format({id:id})).attr({"class":"label label-success"});
                         $("#role_{id} td:eq(2) span".format({id:id})).text("正常");
                         $("#role_{id} td:eq(3) button.btn-success i[class='glyphicon glyphicon-play']".format({id:id})).attr("class", "glyphicon glyphicon-stop");
                         $("#role_{id} td:eq(3) button.btn-success".format({id:id})).attr("class", "btn btn-xs btn-danger");
                     }
                  }
               }
      });
}

function edit_role(id){ // 编辑某一个role的状态
  hidden_module_form();
   var name = $("#role_{id} td:eq(1)".format({id:id})).text();
   $("#role_form .pull-left").text("修改");
   $("#role_form input[name='name']").attr("readonly","readonly");
   $("#role_form input[name='name']").val(name);
   create_module_checkbox();
   full_module_checkbox(id);
   $("#role_form input[name='role_id']").val(id);
   $("#roleform").show(500);
   $('body,html').animate({ scrollTop: 0 }, 500);
}

function add_role(){  // 点击新增按钮事件
  hidden_module_form();
  $("#role_form .pull-left").text("新增");
  $("#role_form input[name='name']").removeAttr("readonly");
  $("#role_form input[name='name']").val("");
  create_module_checkbox();
  $("#role_form input[name='role_id']").val(-1);
  $("#roleform").show(500);
  $('body,html').animate({ scrollTop: 0 }, 500);
}

function check_module_checkbox(){  // 检测选中的module_list
   var $module_list_dom = $("#role_form input[name=module_list]");
   var data={};
  $.each($module_list_dom, function(n, values){
     if (values.checked){
       data[values.value] = 1;
     }else{
       data[values.value] = 0;
     }
  })
  return JSON.stringify(data);


}

function add_edit_role(button){ // role表单的确定按钮
  $(button).attr("disabled","true");
  var $span_dom = $("#role_form input").next("span");
  $span_dom.css("display","none");
  $span_dom.text("");

  var role_id = $("#role_form input[name='role_id']").val();
  var name = $("#role_form input[name='name']").val();

  if (name.length == 0){
    var $span = $("#role_form input[name='name']").next("span");
    $span.css("display", "block");
    $span.text("请输入角色名!");
    $(button).removeAttr("disabled");
    return
  }
  var role_module_data = check_module_checkbox();
  var role_data = {
        "role_id":role_id,
        "name":name,
        "module_list":role_module_data
      };

  if (role_id == -1){
    $.ajax({
            url:"/admin/api/role",
            async:false,
            type:'POST',
            data:role_data,
            success:function(data){
              if(data.code==201){
                 alert(data.info);
                 get_role();
                 create_role_table();
                 hidden_role_form();
              }
              else if(data.code==422){
                 var $span_dom = $("#role_form input[name='{name}']".format({name:data.name})).next("span");
                 $span_dom.css("display","block");
                 $span_dom.text(data.info);
              }
            }
          });
  }else{
    $.ajax({
       url:"/admin/api/role_module",
       async:false,
       type:'POST',
       data:role_data,
       success:function(data){
         alert(data.message);
       }
    })

  }
  $(button).removeAttr("disabled");
}


/*-------------------------------------------------*/


function create_module_table(){ // 填充module表
  $("#module tbody").empty();
  $.each(module_data.data, function(n, values){
      var tr_dom = $("<tr></tr>",{id:"module_{id}".format({id:values.id})});
      $("<td></td>",{text:values.id}).appendTo(tr_dom);
      $("<td></td>",{text:values.name}).appendTo(tr_dom);
      $("<td></td>",{text:values.url}).appendTo(tr_dom);
      $("<td></td>",{text:values.icon_url}).appendTo(tr_dom);

      if (values.status==1){
        $("<td><span class='label label-success'>正常</span></td>").appendTo(tr_dom);
      }else if (values.status==0){
        $("<td><span class='label label-danger'>停用</span></td>").appendTo(tr_dom);
      }else{
        $("<td><span class='label label-danger'>非正常</span></td>").appendTo(tr_dom);
      }
      if (values.status==1){
          $("<td><button class='btn btn-xs btn-warning' onclick='edit_module({id})'><i class='icon-pencil'></i></button>\
          <button class='btn btn-xs btn-danger' onclick='change_module_status({id})'><i class='glyphicon glyphicon-stop'></i></button></td>".format({id:values.id})).appendTo(tr_dom);
      }else if (values.status==0){
        $("<td><button class='btn btn-xs btn-warning' onclick='edit_module({id})'><i class='icon-pencil'></i></button>\
          <button class='btn btn-xs btn-success' onclick='change_module_status({id})'><i class='glyphicon glyphicon-play'></i></button></td>".format({id:values.id})).appendTo(tr_dom);
      }
      tr_dom.appendTo("#module tbody");
  });
}

function create_module_checkbox(){ // 填充module checkbox的数据
   $("#module_list").empty();
   $.each(module_data.data, function(n, values){
     var one=$("<label class='checkbox-inline'><input type='checkbox' name='module_list' value='{id}'> {name} </label>".format({id:values.id, name:values.name}));
     one.appendTo("#module_list");
   })
}

function full_module_checkbox(id){ // 填充module checkbox的选项
   $.get("/admin/api/role_module",param={role_id:id},function(data){
       $.each(data.data, function(n, values){
          $("input[name=module_list][value={value}]".format({value:values})).attr("checked",'true');
       })
   })
}

function change_module_status(id){ // 点击 改变module 按钮事件
  $.ajax({
       url:"/admin/api/module/{id}".format({id:id}),
       async:false,
       type:"DELETE",
       // data:{uid:id},
       success:function(data){
                  if (data.status == 1){
                     if (data.module_status == 0){
                         $("#module_{id} td:eq(4) span".format({id:id})).attr({"class":"label label-danger"});
                         $("#module_{id} td:eq(4) span".format({id:id})).text("停用");
                         $("#module_{id} td:eq(5) button.btn-danger i[class='glyphicon glyphicon-stop']".format({id:id})).attr("class", "glyphicon glyphicon-play");
                         $("#module_{id} td:eq(5) button.btn-danger".format({id:id})).attr("class", "btn btn-xs btn-success");
                     }
                     else if (data.module_status == 1){
                         $("#module_{id} td:eq(4) span".format({id:id})).attr({"class":"label label-success"});
                         $("#module_{id} td:eq(4) span".format({id:id})).text("正常");
                         $("#module_{id} td:eq(5) button.btn-success i[class='glyphicon glyphicon-play']".format({id:id})).attr("class", "glyphicon glyphicon-stop");
                         $("#module_{id} td:eq(5) button.btn-success".format({id:id})).attr("class", "btn btn-xs btn-danger");
                     }
                  }
               }
      });
}

function edit_module(id){ // 点击 编辑module 按钮事件
  hidden_role_form();
  var name = $("#module_{id} td:eq(1)".format({id:id})).text();
  var url = $("#module_{id} td:eq(2)".format({id:id})).text();
  var icon_url = $("#module_{id} td:eq(3)".format({id:id})).text();
  $("#module_form .pull-left").text("修改");
  $("#module_form input[name='name']").attr("readonly","readonly");
  $("#module_form input[name='name']").val(name);
  $("#module_form input[name='url']").val(url)
  $("#module_form input[name='icon_url']").val(icon_url)
  $("#module_form input[name='module_id']").val(id);
  $("#moduleform").show(500);
  $('body,html').animate({ scrollTop: 0 }, 500);
}

function add_module(){ // 点击 新增module 按钮事件
  hidden_role_form();
  $("#module_form .pull-left").text("新增");
  $("#module_form input[name='name']").removeAttr("readonly");
  $("#module_form input[name='name']").val("");
  $("#module_form input[name='url']").val("")
  $("#module_form input[name='icon_url']").val("")
  $("#module_form input[name='module_id']").val(-1);
  $("#moduleform").show(500);
  $('body,html').animate({ scrollTop: 0 }, 500);
}

function add_edit_module(button){ // module表单点击 确定 按钮事件
  $(button).attr("disabled","true");
  var $span_dom = $("#module_form input").next("span");
  $span_dom.css("display","none");
  $span_dom.text("");

  var module_id = $("#module_form input[name='module_id']").val();
  var name = $("#module_form input[name='name']").val();
  var url = $("#module_form input[name='url']").val();
  var icon_url = $("#module_form input[name='icon_url']").val();

  if (name.length == 0){
    var $span = $("#module_form input[name='name']").next("span");
    $span.css("display", "block");
    $span.text("请输入模块名!");
    $(button).removeAttr("disabled");
    return
  }
  if (url.length == 0){
    var $span = $("#module_form input[name='url']").next("span");
    $span.css("display", "block");
    $span.text("请输入url!");
    $(button).removeAttr("disabled");
    return
  }
  if (icon_url.length == 0){
    var $span = $("#module_form input[name='icon_url']").next("span");
    $span.css("display", "block");
    $span.text("请选择icon_url");
    $(button).removeAttr("disabled");
    return
  }

   var module_data={
      name:name,
      url:url,
      icon_url:icon_url
   }

   if (module_id == -1){
     $.ajax({
             url:"/admin/api/module",
             async:false,
             type:'POST',
             data:module_data,
             success:function(data){
               if(data.code==201){
                  alert(data.info);
                  get_module();
                  create_module_table();
                  create_module_checkbox();
                  hidden_module_form();
               }
               else if(data.code==422){
                  var $span_dom = $("#module_form input[name='{name}']".format({name:data.name})).next("span");
                  $span_dom.css("display","block");
                  $span_dom.text(data.info);
               }
             }
           })
   }else{
     $.ajax({
             url:"/admin/api/module/{module_id}".format({module_id:module_id}),
             async:false,
             type:'PATCH',
             data:module_data,
             success:function(data){
               if(data.code==201){
                  alert(data.info);
                  get_module();
                  create_module_table();
               }
               else if(data.code==422){
                  var $span_dom = $("#module_form input[name='{name}']".format({name:data.name})).next("span");
                  $span_dom.css("display","block");
                  $span_dom.text(data.info);
               }
             }
           })
   }
   $(button).removeAttr("disabled");



}

function get_all_data(){ // 获取所有数据
  get_role();
  get_module();
}
function create_all_table(){ // 填充所有表的数据
  create_role_table();
  create_module_table();
  create_module_checkbox();
}

window.onload = function () {
  $('#roleform .wclose').unbind('click').click(function(){
    hidden_form();
  });
  $('#moduleform .wclose').unbind('click').click(function(){
    hidden_form();
  });
  get_all_data();
  create_all_table();
}


function input_on_change(input){ // 在input被修改时, 去除多余的空格
  var temp = $(input).val().Trim();
  $(input).val(temp);
}
