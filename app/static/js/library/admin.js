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

var user_chart = echarts.init(document.getElementById('user_pie'));
var books_chart = echarts.init(document.getElementById('books_pie'));
var histroy_chart = echarts.init(document.getElementById('history_pie'));
var csrftoken = $('meta[name=csrf-token]').attr('content');
var sex_dic={"男":1, "女":2, "其他":3}
function init_pie(){
  user_chart.setOption({
      title : {
        text: '性别分布',
        x:'center',
      },
      tooltip : {
        trigger: 'item',
        formatter: "{b}:{c}({d}%)"
      },
      color:['#009de9','#e0077b','#7753c6'] // 男 女 其他
  });

  books_chart.setOption({
      title : {
        text: '书目分布',
        x:'center',
      },
      tooltip : {
        trigger: 'item',
        formatter: "{b}:{c}({d}%)"
      }
  });
  histroy_chart.setOption({
      title : {
        text: '借阅统计',
        x:'center',
      },
      tooltip : {
        trigger: 'item',
        formatter: "{b}:{c}({d}%)"
      }
  })
}

function get_data(){
  $.get("/Library/admin/pie_data",function(data){
     user_chart.setOption({
        series:[{
          radius: '55%',
          type:'pie',
          data:data.user_data
        }]
     });
     books_chart.setOption({
        series:[{
          radius: ['50%','55%'],
          type:'pie',
          data:data.book_publisher
        },{
          radius: [0,'40%'],
          type:'pie',
          selectedMode: 'single',
          label: {
                normal: {
                    position: 'inner'
                }
            },
            labelLine: {
                normal: {
                    show: false
                }
            },
          data:data.book_publisher_time_data
        }]
     });
     histroy_chart.setOption({
        series:[{
          radius : '55%',
          type:'pie',
          data:data.history_data
        }]
     });
  })
}


$('#myModal').on('show.bs.modal', function (e) {
   var btn = $(e.relatedTarget);
   var title = btn.attr("data-title");
   var content = btn.attr("data-content");
   $("#myModalLabel").text(title);
   $(".modal-body").text(content);
})


user_chart.on('click', function(param){
  var sex = param.data.name;
  sex = sex_dic[sex];
  $.get('/Library/admin/user_data',{sex:sex},function(data){
    create_table(data,'user');
  })
})

books_chart.on('click', function(param){
  $.get('/Library/admin/book_data',function(data){
    create_table(data,'books');
  })
})

histroy_chart.on('click', function(param){
  $.get('/Library/admin/history',function(data){
    console.log(data);
    create_table(data,'history');
  })
})


function create_table(data, table_name){
   var table_dom = $("#table");
   table_dom.empty();
   if (table_name == "user"){
     $('#table_title').text('用户信息');
     create_user_table(data.data);
   }else if(table_name == 'books'){
     $('#table_title').text('书目信息');
     create_books_table(data);
   }else if(table_name == 'history'){
     $("#table_title").text('借阅信息');
     create_histroy_table(data);
   }

}

function create_user_table(data){
    var thead_dom = $("<thead></thead>");
    var tr_dom = $("<tr></tr>");
    var table = $("#table");
    tr_dom.append("<th>用户名</th>");
    tr_dom.append("<th>昵称</th>");
    tr_dom.append("<th>性别</th>");
    tr_dom.append("<th>地址</th>");
    tr_dom.append("<th>电话</th>");
    thead_dom.append(tr_dom);
    table.append(thead_dom);
    var tbody_dom = $("<tbody></tbody>")
    $.each(data, function(n,value){
       tr_dom = $("<tr></tr>");
       tr_dom.append("<td>" + value.user_name + "</td>");
       tr_dom.append("<td>" + value.lib_name + "</td>");
       if(value.sex == 1){
         tr_dom.append("<td>男</td>");
       }else if (value.sex == 2){
         tr_dom.append("<td>女</td>");
       }else{
         tr_dom.append("<td>其他</td>");
       }
       tr_dom.append("<td>" + value.address +"</td>");
       tr_dom.append("<td>" + value.phone +"</td>");
       tbody_dom.append(tr_dom);
    });
    table.append(tbody_dom);

}

function create_books_table(data){
    var thead_dom = $("<thead></thead>");
    var tr_dom = $("<tr></tr>");
    var table = $("#table");
    tr_dom.append("<th>书名</th>");
    tr_dom.append("<th>分类</th>");
    tr_dom.append("<th>作者</th>");
    tr_dom.append("<th>出版社</th>");
    tr_dom.append("<th>出版时间</th>");
    tr_dom.append("<th>介绍</th>");
    tr_dom.append("<th>状态</th>");
    tr_dom.append("<th>所有者</th>")
    tr_dom.append("<th>借书人</th>");
    thead_dom.append(tr_dom);
    table.append(thead_dom);
    var tbody_dom = $("<tbody></tbody>")
    $.each(data.data, function(n,value){
       tr_dom = $("<tr></tr>");
       tr_dom.append("<td>" + value.name + "</td>");
       tr_dom.append("<td style='overflow:hidden;white-space:nowrap;text-overflow:ellipsis;'>" + value.classify + "</td>");
       tr_dom.append("<td style='overflow:hidden;white-space:nowrap;text-overflow:ellipsis;'>" + value.author + "</td>");
       tr_dom.append("<td>" + value.publisher +"</td>");
       tr_dom.append("<td>" + value.publish_time +"</td>");
       var button_dom = $("<button type='button' class='btn btn-info' data-title='{name}' data-content='{desc}' data-toggle='modal' data-target='#myModal'>详细</button>".format({name:value.name, desc:value.desc}));
       var td_dom = $("<td></td>");
       td_dom.append(button_dom);
       tr_dom.append(td_dom);
       if (value.status == 0){
         tr_dom.append("<td><h4><span class='label label-primary'>空闲</span></h4></td>");
       }else if(value.status==1){
         tr_dom.append("<td><h4><span class='label label-warning'>预定中</span></h4></td>");
       }else if(value.status==2){
         tr_dom.append("<td><h4><span class='label label-danger'>借出中</span></h4></td>");
       }else if(value.status==-1){
         tr_dom.append("<td><h4><span class='label label-default'>下架</span></h4></td>");
       };
       tr_dom.append("<td>" + value.lender_name + "</td>")
       tr_dom.append("<td>" + value.borrower_name + "</td>");
       tbody_dom.append(tr_dom);
    });
    if (data.pre_href.length>0||data.next_href.length>0){
      var last_row = $("<tr></tr>");
      var last_td = $("<td colspan='8'></td>")
      if (data.pre_href.length>0){
        last_td.append("<button type='button' class='btn btn-info' data-url={url} onclick='books_next(this)'>上一页</button>".format({url:data.pre_href}))
      }
      if (data.next_href.length>0){
        last_td.append("<button type='button' class='btn btn-info' data-url={url} onclick='books_next(this)'>下一页</button>".format({url:data.next_href}))
      }
      last_row.append(last_td);
      tbody_dom.append(last_row);
    }
    table.append(tbody_dom);
}

function create_histroy_table(data){
    var thead_dom = $("<thead></thead>");
    var tr_dom = $("<tr></tr>");
    var table = $("#table");
    tr_dom.append("<th>书名</th>");
    tr_dom.append("<th>出借人</th>");
    tr_dom.append("<th>借书人</th>");
    tr_dom.append("<th>预定时间</th>");
    tr_dom.append("<th>出借时间</th>");
    tr_dom.append("<th>归还时间</th>");
    tr_dom.append("<th>当前状态</th>");
    thead_dom.append(tr_dom);
    table.append(thead_dom);
    var tbody_dom = $("<tbody></tbody>")
    $.each(data.data, function(n,value){
       tr_dom = $("<tr></tr>");
       tr_dom.append("<td>" + value.book_name + "</td>");
       tr_dom.append("<td>" + value.lender_name + "</td>");
       tr_dom.append("<td>" + value.borrower_name + "</td>");
       tr_dom.append("<td>" + value.create_time +"</td>");
       tr_dom.append("<td>" + value.borrow_time +"</td>");
       tr_dom.append("<td>" + value.return_time +"</td>");
       if (value.action == 1){
          tr_dom.append("<td><h4><span class='label label-primary status'>出借</span></h4></td>");
       }else if(value.action == 2){
         tr_dom.append("<td><h4><span class='label label-success status'>归还</span></h4></td>");
       }else if(value.action == 3){
         tr_dom.append("<td><h4><span class='label label-warning status'>预定</span></h4></td>");
       }else if(value.action == 4){
         tr_dom.append("<td><h4><span class='label label-danger status'>拒绝</span></h4></td>");
       }
       tbody_dom.append(tr_dom);
    });
    if (data.pre_href.length>0||data.next_href.length>0){
      var last_row = $("<tr></tr>");
      var last_td = $("<td colspan='8'></td>")
      if (data.pre_href.length>0){
        last_td.append("<button type='button' class='btn btn-info' data-url={url} onclick='history_next(this)'>上一页</button>".format({url:data.pre_href}))
      }
      if (data.next_href.length>0){
        last_td.append("<button type='button' class='btn btn-info' data-url={url} onclick='history_next(this)'>下一页</button>".format({url:data.next_href}))
      }
      last_row.append(last_td);
      tbody_dom.append(last_row);
    }
    table.append(tbody_dom);
}


function books_next(btn){
   var url = $(btn).attr("data-url");
   $.get(url,function(data){
     create_table(data,'books');
   })
}

function history_next(btn){
   var url = $(btn).attr("data-url");
   $.get(url,function(data){
     create_table(data,'history');
   })
}

$(function() {
   init_pie();
   get_data();
   setInterval('get_data()',3000);
 })
