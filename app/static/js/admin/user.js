
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

function hidden_form(){
  // 隐藏表单
  var $wbox = $("#userform");
  $wbox.hide(500);
}

function hidden_group_form(){
  var $wbox = $("#groupform");
  $wbox.hide(500);
}

var User_data;
var current_user_index;
var User_data_page=1;
var Role_data;
var Group_data;

/*
    针对User表的操作
    通过get_User_data函数，从后端获取数据，存储到全局变量User_data中，
    然后执行show_User_data函数，将数据展示到table中，
    最后执行show_paginate函数，将分页信息展示到表格最下方。

*/
function get_User_data(){ // 获取User数据
    $.get("/admin/api/user", data={'page':User_data_page}, function(data){
       User_data = data.data;
       show_Use_data();
       show_paginate(data.total_page);
    })
}

function show_Use_data(){ // 展示User表
    var tbody = $("#user tbody");
    tbody.empty();
    $.each(User_data, function(n, values){
      var tr_dom = $("<tr></tr>");
      $("<td>{id}</td>".format({id:n+1})).appendTo(tr_dom);
      $("<td>{name}</td>".format({name:values.name})).appendTo(tr_dom);
      $("<td>{password}</td>".format({password:values.password})).appendTo(tr_dom);
      $("<td>{token}</td>".format({token:values.token})).appendTo(tr_dom);
      $("<td>{role_name}</td>".format({role_name:values.role_name})).appendTo(tr_dom);
      if(values.sex == 0){
        $("<td>男</td>").appendTo(tr_dom);
      }else if (values.sex==1) {
        $("<td>女</td>").appendTo(tr_dom);
      }else{
        $("<td>其他</td>").appendTo(tr_dom);
      }

      if (values.status==1){
        $("<td id='user_{id}_status'><span class='label label-success'>正常</span></td>".format({id:n})).appendTo(tr_dom);
      }else if (values.status==0){
        $("<td id='user_{id}_status'><span class='label label-danger'>停用</span></td>".format({id:n})).appendTo(tr_dom);
      }else{
        $("<td id='user_{id}_status'><span class='label label-danger'>非正常</span></td>".format({id:n})).appendTo(tr_dom);
      }
      if (values.status==1){
          $("<td id='user_{id}_control'><button class='btn btn-xs btn-warning' onclick='edit_user({id})'><i class='icon-pencil'></i></button>\
          <button class='btn btn-xs btn-danger' onclick='change_user_status({id})'><i class='glyphicon glyphicon-stop'></i></button></td>".format({id:n})).appendTo(tr_dom);
      }else if (values.status==0){
        $("<td id='user_{id}_control'><button class='btn btn-xs btn-warning' onclick='edit_user({id})'><i class='icon-pencil'></i></button>\
          <button class='btn btn-xs btn-success' onclick='change_user_status({id})'><i class='glyphicon glyphicon-play'></i></button></td>".format({id:n})).appendTo(tr_dom);
      }
      tr_dom.appendTo(tbody);
    });
}

function show_paginate(totalpages){ // 分页
  var pagination_dom = $("#user_pagination");
  pagination_dom.bs_pagination("destroy");
  if (totalpages<=1){
     pagination_dom.attr("hidden","true");
  }else{
     pagination_dom.removeAttr("hidden");
  }
  pagination_dom.bs_pagination({
     currentPage: User_data_page,
     totalPages: totalpages,
     visiblePageLinks: 8,
     showGoToPage: true,
     showRowsPerPage: false,
     showRowsInfo: false,
     showRowsDefaultInfo: false,
     onChangePage: function(event, data) { // returns page_num and rows_per_page after a link has clicked
        var currentPage = data.currentPage;
        if (currentPage != User_data_page){
          User_data_page = currentPage;
          get_User_data();
        }
     },
     onLoad: function() { // returns page_num and rows_per_page on plugin load
     }
  });
}

function edit_user(id){ // 用户表 点击 编辑 按钮
    current_user_index = id;
    hidden_group_form();
    var $all_span = $("input").next("span");
    $all_span.css("display","none");
    $all_span.text("");

    var name = User_data[id].name;
    var password = User_data[id].password;
    var role_id = User_data[id].role_id;
    var sex = User_data[id].sex;
    full_group_list();

    $("#userform .pull-left").text("修改");
    $("#userform form input[name='username']").val(name);
    $("#userform form input[name='username']").attr("readonly","readonly");
    $("#userform form input[name='password']").val(password);
    $("#userform form input[name='sex']").removeAttr("checked");
    $("#userform form input[name='sex'][value='{sex}']".format({sex:sex})).prop("checked","true");
    $("#userform form select").val(role_id);
    $("#userform form input[name='uid']").val(User_data[id].id);
    $("#userform").show(500);
    $('body,html').animate({ scrollTop: 0 }, 500);
}

function add_user(){ // 用户表格下方的 新增 按钮点击事件
    current_user_index = -1;
    hidden_group_form();
    var $all_span = $("input").next("span");
    $all_span.css("display","none");
    $all_span.text("");

    var name = "";
    var password = "";
    var role_id = 1;
    var sex=2;
    show_Group_data_in_User_form();

    $("#userform .pull-left").text("新增");
    $("#userform form input[name='username']").val(name);
    $("#userform form input[name='username']").removeAttr("readonly");
    $("#userform form input[name='password']").val(password);
    $("#userform form input[name='sex']").removeAttr("checked");
    $("#userform form input[name='sex'][value='{sex}']".format({sex:sex})).attr("checked","true");
    $("#userform form select").val(role_id);
    $("#userform form input[name='uid']").val(-1);
    $("#userform").show(500);
    $('body,html').animate({ scrollTop: 0 }, 500);
}

function change_user_status(id){   //点击删除启用按钮事件
   $.ajax({
        url:"/admin/api/user/{id}".format({id:User_data[id].id}),
        async:false,
        type:"DELETE",
        success:function(data){
          console.log(data);
                   if (data.status == 1){
                      if (data.user_status == 0){
                          $("#user_{id}_status span".format({id:id})).attr({"class":"label label-danger"});
                          $("#user_{id}_status span".format({id:id})).text("停用");
                          $("#user_{id}_control button.btn-danger i[class='glyphicon glyphicon-stop']".format({id:id})).attr("class", "glyphicon glyphicon-play");
                          $("#user_{id}_control button.btn-danger".format({id:id})).attr("class", "btn btn-xs btn-success");
                      }
                      else if (data.user_status == 1){
                          $("#user_{id}_status span".format({id:id})).attr({"class":"label label-success"});
                          $("#user_{id}_status span".format({id:id})).text("正常");
                          $("#user_{id}_control button.btn-success i[class='glyphicon glyphicon-play']".format({id:id})).attr("class", "glyphicon glyphicon-stop");
                          $("#user_{id}_control button.btn-success".format({id:id})).attr("class", "btn btn-xs btn-danger");
                      }
                      User_data[id].status = data.user_status;
                   }
                }
       });
}

function add_edit_user(button){ // 提交用户表单
  $(button).attr("disabled","true");
  var $span_dom = $("#userform input").next("span");
  $span_dom.css("display","none");
  $span_dom.text("");

  var uid = $("input[name='uid']").val();
  var username = $("input[name='username']").val();
  var password = $("input[name='password']").val();
  var role_id = $("select[name='role_id']").val();
  var sex = $("input[name='sex']:checked").val();
  console.log(sex);
  var group_list = check_group();

  if (username.length == 0){
    var $span = $("#userform input[name='username']").next("span");
    $span.css("display", "block");
    $span.text("请输入用户名!");
    $(button).removeAttr("disabled");
    return;
  }

  if (password.length == 0){
    var $span = $("#userform input[name='password']").next("span");
    $span.css("display", "block");
    $span.text("请输入密码!");
    $(button).removeAttr("disabled");
    return;
  }

  var form_data = {
    "name":username,
    "password":password,
    "role_id":role_id,
    "group_list":group_list,
    "sex":sex
  }
  if (uid == -1){
    $.ajax({
      url:"/admin/api/user",
      async:false,
      type:'POST',
      data:form_data,
      success:function(data){
        if(data.code==201){
           alert(data.info);
           get_User_data();
           hidden_form();
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
      url:"/admin/api/user/{uid}".format({uid:uid}),
      async:false,
      type:'PATCH',
      data:form_data,
      success:function(data){
        if(data.code==201){
           alert(data.info);
           get_User_data();
           hidden_form();
        }
        else if(data.code==422){
           var $span_dom = $("#role_form input[name='{name}']".format({name:data.name})).next("span");
           $span_dom.css("display","block");
           $span_dom.text(data.info);
        }
      }
    });
  }
  $(button).removeAttr("disabled");


}

function check_group(){ // 检验group_list的选项
  var data={};
  var $group_list_dom = $("#group_list input[name='group_list']");
  $.each($group_list_dom, function(n, values){
    if (values.checked){
      data[values.value] = 1;
    }else{
      data[values.value] = 0;
    }
  })
  return JSON.stringify(data);
}

function full_group_list(){ // 填充group_list的选项
    id = current_user_index;
    show_Group_data();
    if (id == -1){
      return;
    }
    $.get("/admin/api/user_group",param={user_id:User_data[id].id},function(data){
        $.each(data.data, function(n, values){
           $("input[name=group_list][value={value}]".format({value:values})).attr("checked",'true');
        })
    });
}
/*
   针对角色表的操作
   通过get_Role_data函数获取角色表信息，存入Role_data全局变量
   然后执行show_Role_data函数, 将数据展示到用户表单里的select中。
*/


function get_Role_data(){ // 获取角色表数据
  $.get("/admin/api/role", function(data){
      Role_data = data.data;
      show_Role_data();

  })
}

function show_Role_data(){ // 填充角色表数据至用户表单的 select 中
  var role_list = $("#role_list");
  role_list.empty();
  $.each(Role_data, function(n, values){
      $("<option value={id}>{name}</option>".format({id:values.id, name:values.name})).appendTo(role_list);
  });
}

/*
   针对分组表的操作
   通过get_Group_data函数获取角色表信息，存入Group_data全局变量
   然后执行show_Group_data函数, 将数据展示到table中。
*/


function get_Group_data(){ // 获取所有分组信息
  $.get("/admin/api/group_list", function(data){
      Group_data = data.data;
      show_Group_data();
  })
}

function show_Group_data(){ // 展示分组信息表
  var group = $("#group tbody");
  group.empty();
  $.each(Group_data, function(n, values){
    var tr_dom = $("<tr></tr>");
    $("<td>{id}</td>".format({id:n+1})).appendTo(tr_dom);
    $("<td>{name}</td>".format({name:values.name})).appendTo(tr_dom);
    if (values.status==1){
      $("<td id='group_{id}_status'><span class='label label-success'>正常</span></td>".format({id:n})).appendTo(tr_dom);
    }else if (values.status==0){
      $("<td id='group_{id}_status'><span class='label label-danger'>停用</span></td>".format({id:n})).appendTo(tr_dom);
    }else{
      $("<td id='group_{id}_status'><span class='label label-danger'>非正常</span></td>".format({id:n})).appendTo(tr_dom);
    }
    if (values.status==1){
        $("<td id='group_{id}_control'><button class='btn btn-xs btn-warning' onclick='edit_group({id})'><i class='icon-pencil'></i></button>\
        <button class='btn btn-xs btn-danger' onclick='change_group_status({id})'><i class='glyphicon glyphicon-stop'></i></button></td>".format({id:n})).appendTo(tr_dom);
    }else if (values.status==0){
      $("<td id='group_{id}_control'><button class='btn btn-xs btn-warning' onclick='edit_group({id})'><i class='icon-pencil'></i></button>\
        <button class='btn btn-xs btn-success' onclick='change_group_status({id})'><i class='glyphicon glyphicon-play'></i></button></td>".format({id:n})).appendTo(tr_dom);
    }
    tr_dom.appendTo(group);
  });
  show_Group_data_in_User_form();
}

function show_Group_data_in_User_form(){ // 将分组信息填充到用户表单的 group_list div中
  var group_list = $("#group_list");
  group_list.empty();
  $.each(Group_data, function(n, values){
    if(values.status == 1){
      $("<label class='checkbox-inline'><input type='checkbox' name='group_list' value='{id}'> {name} </label>".format({id:values.id, name:values.name})).appendTo(group_list);

    }
  })
}

function edit_group(id){ // 点击 分组信息编辑 按钮事件
  hidden_form();
  var $all_span = $("input").next("span");
  $all_span.css("display","none");
  $all_span.text("");

  var name = Group_data[id].name;

  $("#groupform .pull-left").text("修改");
  $("#groupform form input[name='group_name']").val(name);
  $("#groupform form input[name='group_id']").val(Group_data[id].id);
  $("#groupform").show(500);
  $('body,html').animate({ scrollTop: 0 }, 500);
}

function add_group(){  // 点击 新增分组信息 按钮事件
  hidden_form();
  var $all_span = $("input").next("span");
  $all_span.css("display","none");
  $all_span.text("");

  var name = "";

  $("#groupform .pull-left").text("新增");
  $("#groupform form input[name='group_name']").val(name);
  $("#groupform form input[name='group_id']").val(-1);
  $("#groupform").show(500);
  $('body,html').animate({ scrollTop: 0 }, 500);
}

function change_group_status(id){ // 点击 分组信息的修改状态 按钮
   $.ajax({
        url:"/admin/api/group_list/{id}".format({id:Group_data[id].id}),
        async:false,
        type:"DELETE",
        success:function(data){
          console.log(data);
                   if (data.status == 1){
                      if (data.group_status == 0){
                          $("#group_{id}_status span".format({id:id})).attr({"class":"label label-danger"});
                          $("#group_{id}_status span".format({id:id})).text("停用");
                          $("#group_{id}_control button.btn-danger i[class='glyphicon glyphicon-stop']".format({id:id})).attr("class", "glyphicon glyphicon-play");
                          $("#group_{id}_control button.btn-danger".format({id:id})).attr("class", "btn btn-xs btn-success");
                      }
                      else if (data.group_status == 1){
                          $("#group_{id}_status span".format({id:id})).attr({"class":"label label-success"});
                          $("#group_{id}_status span".format({id:id})).text("正常");
                          $("#group_{id}_control button.btn-success i[class='glyphicon glyphicon-play']".format({id:id})).attr("class", "glyphicon glyphicon-stop");
                          $("#group_{id}_control button.btn-success".format({id:id})).attr("class", "btn btn-xs btn-danger");
                      }
                      Group_data[id].status = data.group_status;
                   }
                  show_Group_data_in_User_form();
                  full_group_list();
                }
       });
}

function add_edit_group(button){
  $(button).attr("disabled","true");
  var $span_dom = $("#groupform input").next("span");
  $span_dom.css("display","none");
  $span_dom.text("");

  var group_id = $("input[name='group_id']").val();
  var name = $("input[name='group_name']").val();


  if (name.length == 0){
    var $span = $("#groupform input[name='username']").next("span");
    $span.css("display", "block");
    $span.text("请输入分组名!");
    $(button).removeAttr("disabled");
    return;
  }

  var form_data = {
    "name":name,
  }
  if (group_id == -1){
    $.ajax({
      url:"/admin/api/group_list",
      async:false,
      type:'POST',
      data:form_data,
      success:function(data){
        if(data.code==201){
           alert(data.info);
           get_Group_data();
           hidden_group_form();
        }
      }
    });
  }else{
    $.ajax({
      url:"/admin/api/group_list/{group_id}".format({group_id:group_id}),
      async:false,
      type:'PATCH',
      data:form_data,
      success:function(data){
        if(data.code==201){
           alert(data.info);
           get_Group_data();
           hidden_group_form();
        }
        else if(data.code==422){
           var $span_dom = $("#groupform input[name='{name}']".format({name:data.name})).next("span");
           $span_dom.css("display","block");
           $span_dom.text(data.info);
        }
      }
    });
  }
  $(button).removeAttr("disabled");
}

window.onload = function () {
  get_User_data();
  get_Role_data();
  get_Group_data();
  $('#userform .wclose').unbind('click').click(function(){
    hidden_form();
  });
  $('#groupform .wclose').unbind('click').click(function(){
    hidden_group_form();
  });
}


function input_on_change(input){
  var temp = $(input).val().Trim();
  $(input).val(temp);
}
