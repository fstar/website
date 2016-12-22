
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


function get_role(page){
  // 获取用户信息表的数据,生成表格
  $.post("/admin/api/get_role", data={"page":page}, function(data){
      $("#user tbody").empty();
      var table_data = data.data;
      console.log(data);
      $.each(table_data, function(n, values){
          // 生成一行数据
          var tr_dom = $("<tr></tr>",{id:values.id});
          $("<td></td>",{text:values.id}).appendTo(tr_dom);
          $("<td></td>",{text:values.name}).appendTo(tr_dom);
          if (values.status==1){
            $("<td id={id}_status><span class='label label-success'>正常</span></td>".format({id:values.id})).appendTo(tr_dom);
          }else if (values.status==0){
            $("<td id={id}_status><span class='label label-danger'>停用</span></td>".format({id:values.id})).appendTo(tr_dom);
          }else{
            $("<td id={id}_status><span class='label label-danger'>非正常</span></td>".format({id:values.id})).appendTo(tr_dom);
          }
          if (values.status==1){
              $("<td id={id}_control><button class='btn btn-xs btn-warning' onclick='edit_role({id})'><i class='icon-pencil'></i></button>\
              <button class='btn btn-xs btn-danger' onclick='change_role_status({id})'><i class='icon-remove'></i></button></td>".format({id:values.id})).appendTo(tr_dom);
          }else if (values.status==0){
            $("<td id={id}_control><button class='btn btn-xs btn-warning' onclick='edit_role({id})'><i class='icon-pencil'></i></button>\
              <button class='btn btn-xs btn-success' onclick='change_role_status({id})'><i class='icon-ok'></i></button></td>".format({id:values.id})).appendTo(tr_dom);
          }
          tr_dom.appendTo("#user tbody");
      });

      if (data.hash_prev){
          $("#user_pagination").append("<li><a href='javascript:void(0)' onclick=get_user("+ (data.current_page-1) +")>Prev</a></li>");
      }
      if (data.has_next){
          $("#user_pagination").append("<li><a href='javascript:void(0)' onclick=get_user("+ (data.current_page+1) +")>next</a></li>");
      }
  })
}

function edit_role(id){
  // 点击编辑按钮事件,
  var $all_span = $("input").next("span");
  $all_span.css("display","none");
  $all_span.text("");
   if (id != -1){
     var tr_dom = $("#{id} td".format({id:id}));
     var name = $(tr_dom[1]).text();
     console.log(id, name);
     $("#userform .pull-left").text("修改");
     $("#userform form input[name='username']").val(name);
     $("#userform form input[name='username']").attr("readonly","readonly");

   }else{
     var name = "";
     $("#userform .pull-left").text("新增");
     $("#userform form input[name='username']").val(name);
     $("#userform form input[name='username']").removeAttr("readonly")
   }
   $("#userform form input[name='role_id']").val(id);
   $.ajax({
      url:"/admin"
   })

   $("#userform").show(500);
   $('body,html').animate({ scrollTop: 0 }, 500);
}

function change_user_status(id){
  //点击删除启用按钮事件
   console.log("change_user_status:"+id);
   $.post("/admin/api/change_user_status", data={uid:id}, function(data){
       if (data.status == 1){
          if (data.user_status == 0){
              $("#{id}_status span".format({id:id})).attr({"class":"label label-danger"});
              $("#{id}_status span".format({id:id})).text("停用");
              $("#{id}_control button.btn-danger i.icon-remove".format({id:id})).attr("class", "icon-ok");
              $("#{id}_control button.btn-danger".format({id:id})).attr("class", "btn btn-xs btn-success");
          }
          else if (data.user_status == 1){
              $("#{id}_status span".format({id:id})).attr({"class":"label label-success"});
              $("#{id}_status span".format({id:id})).text("正常");
              $("#{id}_control button.btn-success i.icon-ok".format({id:id})).attr("class", "icon-remove");
              $("#{id}_control button.btn-success".format({id:id})).attr("class", "btn btn-xs btn-danger");
          }
       }
   })
}

function get_all_role(){
  //获取所有角色信息, 供select填充数据
  $.post("/admin/api/get_role", data={"page":1}, function(data){
      var table_data = data.data;
      console.log(data);
      $.each(table_data, function(n, values){
          $("<option value={id}>{name}</option>".format({id:values.id, name:values.name})).appendTo("#role_list");
      });
  })
}

function hidden_form(){
  // 隐藏表单
  var $wbox = $("#userform");
  $wbox.hide(500);

}

function add_edit_api(button){

  $(button).attr("disabled","true");
   var username = $("input[name='username']").val();
   var password = $("input[name='password']").val();
   var role_id = $("#role_list").val();
   var uid = $("input[name='uid']").val();
   console.log(username, password, role_id, uid);

   if (username.length == 0){
     var $span = $("input[name=username]").next("span");
     $span.css("display", "block");
     $span.text("请输入用户名!");
     $(button).removeAttr("disabled");

     return
   }

   if (password.length == 0){
     var $span = $("input[name=password]").next("span");
     $span.css("display", "block");
     $span.text("请输入密码!");
     $(button).removeAttr("disabled");

     return
   }


   var data={
      "username":username,
      "password":password,
      "role_id":role_id,
      "uid":uid
   }
   $.ajax({
     type:"POST",
     url:'/admin/api/add_edit_user',
     data:data,
     success:function(data){
        if(data.status=='y'){
           alert(data.info);
           get_user(1);
           $(button).removeAttr("disabled");

        }
        else if(data.status=="n"){
           var $span_dom = $("input[name={name}]".format({name:data.name})).next("span");
           $span_dom.css("display","block");
           $span_dom.text(data.info);
           $(button).removeAttr("disabled");
        }
     },
     async:false
 });
}

window.onload = function () {
  get_role(1);
  get_all_module();
  $('#userform .wclose').unbind('click').click(function(){
    hidden_form();
  });
}
