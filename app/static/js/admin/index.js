function get_user(page){
  $.get("/admin/api/user", data={"page":page}, function(data){
      var table_data = data.data;
      console.log(data);
      $.each(table_data, function(n, values){
          var tr_dom = $("<tr></tr>",{id:values.id});
          $("<td></td>",{text:values.id}).appendTo(tr_dom);
          $("<td></td>",{text:values.name}).appendTo(tr_dom);
          $("<td></td>",{text:values.password}).appendTo(tr_dom);
          $("<td></td>",{text:values.token}).appendTo(tr_dom);
          $("<td></td>",{text:values.role_name}).appendTo(tr_dom);
          if (values.status==1){
            $("<td><span class='label label-success'>正常</span></td>").appendTo(tr_dom);
          }else if (values.status==0){
            $("<td><span class='label label-danger'>停用</span></td>").appendTo(tr_dom);
          }else{
            $("<td><span class='label label-danger'>非正常</span></td>").appendTo(tr_dom);
          }
          tr_dom.appendTo("#user tbody");
      });

      if (data.hash_prev){
          var prev_page = parsInt(data.current_page)-1;
          $("#user_pagination").append("<li><a href='javascript:void(0)' onclick=get_user("+ prev_page +")>Prev</a></li>");
      }
      if (data.has_next){
          var next_page = parsInt(data.current_page)+1;
          $("#user_pagination").append("<li><a href='javascript:void(0)' onclick=get_user("+ next_page +")>next</a></li>");
      }
  })
}

function get_role(page){
  $.get("/admin/api/role", function(data){
      var table_data = data.data;
      console.log(data)
      $.each(table_data, function(n, values){
          var tr_dom = $("<tr></tr>",{id:values.id});
          $("<td></td>",{text:values.id}).appendTo(tr_dom);
          $("<td></td>",{text:values.name}).appendTo(tr_dom);
          if (values.status==1){
            $("<td><span class='label label-success'>正常</span></td>").appendTo(tr_dom);
          }else if (values.status==0){
            $("<td><span class='label label-danger'>停用</span></td>").appendTo(tr_dom);
          }else{
            $("<td><span class='label label-danger'>非正常</span></td>").appendTo(tr_dom);
          }
          tr_dom.appendTo("#role tbody");
      });
  })
}

function get_module(page){
  $.get("/admin/api/module", function(data){
      var table_data = data.data;
      console.log(data)
      $.each(table_data, function(n, values){
          var tr_dom = $("<tr></tr>",{id:values.id});
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
          tr_dom.appendTo("#module tbody");
      });
  })
}

function draw_graph(){
  var myChart = echarts.init(document.getElementById('role_module'));

  $.get("/admin/api/get_role_module", function(data){
      console.log(data.nodes);

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
                         roam: false,
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
      })
}
window.onload = function () {
  get_user(1);
  get_role(1);
  get_module(1);
  draw_graph();
}
