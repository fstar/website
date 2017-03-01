
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

var User_data;
var User_data_page=1;
var User_keyword='';

var Role_data;
var Module_data;

/*
    针对User表的操作
    通过get_User_data函数，从后端获取数据，存储到全局变量User_data中，
    然后执行show_User_data函数，将数据展示到table中，
    最后执行show_paginate函数，将分页信息展示到表格最下方。

*/
function get_User_data(){
    $.get("/admin/api/user", data={'page':User_data_page}, function(data){
       User_data = data.data;
       show_Use_data();
       show_paginate(data.total_page);
    })
}

function show_Use_data(){
    var tbody = $("#user tbody");
    tbody.empty();
    $.each(User_data, function(n, values){
      var tr_dom = $("<tr></tr>");
      $("<td>{id}</td>".format({id:n+1})).appendTo(tr_dom);
      $("<td>{name}</td>".format({name:values.name})).appendTo(tr_dom);
      $("<td>{password}</td>".format({password:values.password})).appendTo(tr_dom);
      $("<td>{token}</td>".format({token:values.token})).appendTo(tr_dom);
      $("<td>{role_name}</td>".format({role_name:values.role_name})).appendTo(tr_dom);
      if (values.status==1){
        $("<td><span class='label label-success'>正常</span></td>").appendTo(tr_dom);
      }else if (values.status==0){
        $("<td><span class='label label-danger'>停用</span></td>").appendTo(tr_dom);
      }else{
        $("<td><span class='label label-danger'>非正常</span></td>").appendTo(tr_dom);
      }
      tr_dom.appendTo(tbody);
    });
}

function show_paginate(totalpages){
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


/*
   针对角色表的操作
   通过get_Role_data函数获取角色表信息，存入Role_data全局变量
   然后执行show_Role_data函数, 将数据展示到table中。
*/


function get_Role_data(){
  $.get("/admin/api/role", function(data){
      Role_data = data.data;
      show_Role_data();

  })
}

function show_Role_data(){
  var tbody = $("#role tbody");
  tbody.empty();
  $.each(Role_data, function(n, values){
    var tr_dom = $("<tr></tr>");
    $("<td>{id}</td>".format({id:values.id})).appendTo(tr_dom);
    $("<td>{name}</td>".format({name:values.name})).appendTo(tr_dom);
  if (values.status==1){
      $("<td><span class='label label-success'>正常</span></td>").appendTo(tr_dom);
    }else if (values.status==0){
      $("<td><span class='label label-danger'>停用</span></td>").appendTo(tr_dom);
    }else{
      $("<td><span class='label label-danger'>非正常</span></td>").appendTo(tr_dom);
    }
    tr_dom.appendTo(tbody);
  });
}

/*
   针对Module表的操作
   通过get_Role_data函数获取角色表信息，存入Role_data全局变量
   然后执行show_Role_data函数, 将数据展示到table中。
*/

function get_Module_data(){
  $.get("/admin/api/module", function(data){
      Module_data = data.data;
      show_Module_data();
  })
}

function show_Module_data(){
  var tbody = $("#module tbody");
  tbody.empty();
  $.each(Module_data, function(n, values){
    var tr_dom = $("<tr></tr>");
    $("<td>{id}</td>".format({id:values.id})).appendTo(tr_dom);
    $("<td>{name}</td>".format({name:values.name})).appendTo(tr_dom);
    $("<td>{url}</td>".format({url:values.url})).appendTo(tr_dom);
    $("<td>{icon_url}</td>".format({icon_url:values.icon_url})).appendTo(tr_dom);
  if (values.status==1){
      $("<td><span class='label label-success'>正常</span></td>").appendTo(tr_dom);
    }else if (values.status==0){
      $("<td><span class='label label-danger'>停用</span></td>").appendTo(tr_dom);
    }else{
      $("<td><span class='label label-danger'>非正常</span></td>").appendTo(tr_dom);
    }
    tr_dom.appendTo(tbody);
  });
}

function draw_graph(){
  var myChart = echarts.init(document.getElementById('role_module'));
  $.get("/admin/api/get_role_module", function(data){
    if (data.nodes.length==0){
      return;
    }
      var option = {
                title: {
                   text: '角色模块关系图'
                },
                animationDurationUpdate: 1500,
                animationEasingUpdate: 'quinticInOut',
                series : [
                    {
                         type: 'graph',
                         layout: 'force',
                        //  progressiveThreshold: 700,
                         data: data.nodes,
                         edges: data.edges,
                         slient:true,

                         force:{
                            // edgeLength:[100, 300]
                            repulsion:1000
                         },
                         label: {
                            normal:{
                              position: 'right',
                              show: true
                            },
                             emphasis: {
                                 position: 'right',
                                 show: true
                             }
                         },
                         roam: true,
                         focusNodeAdjacency: true,
                         lineStyle: {
                             normal: {
                                 width: 0.5,
                                 curveness: 0,
                                 opacity: 0.7
                             }
                         }
                     }
                  ]
        };
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
      });

   var user_group_chart = echarts.init(document.getElementById('user_group'));
   $.get("/admin/api/get_user_group", function(data){
       if (data.nodes.length==0){
         return;
       }
       var option = {
                 title: {
                    text: '用户分组关系图'
                 },
                 animationDurationUpdate: 1500,
                 animationEasingUpdate: 'quinticInOut',
                 series : [
                     {
                          type: 'graph',
                          layout: 'force',
                         //  progressiveThreshold: 700,
                          data: data.nodes,
                          edges: data.edges,
                          slient:true,
                          roam:true,
                          force:{
                             // edgeLength:[100, 300]
                             repulsion:1000
                          },
                          label: {
                             normal:{
                               position: 'right',
                               show: true
                             },
                              emphasis: {
                                  position: 'right',
                                  show: true
                              }
                          },
                          focusNodeAdjacency: true,
                          lineStyle: {
                              normal: {
                                  width: 0.5,
                                  curveness: 0,
                                  opacity: 0.7
                              }
                          }
                      }
                   ]
         };
         // 使用刚指定的配置项和数据显示图表。
         user_group_chart.setOption(option);
       });
}
window.onload = function () {
  get_User_data();
  get_Role_data();
  get_Module_data();
  draw_graph();
}
