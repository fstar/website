$(document).ready(function() {
    read_data();
});
function showUnreadNews()
{
    $(document).ready(function() {
        read_data();
    });
}
setInterval('showUnreadNews()',5000);

function read_data(){
  $.ajax({
      type: "GET",
      url: "/index/total_data",
      dataType: "json",
      success: function(msg) {
          company_spark_line(msg);
          job_spark_line(msg);
      }
  });
}

function company_spark_line(msg){
  // 信息来源-公司数量统计
      var company_query = msg.company_query;
      var company_count = msg.company_count;
      var values = new Array();
      var names = new Array();
      $.each(company_query, function(n,value){
         names.push(value.from_web);
         values.push(value.count);
      });
      $("#company_query").sparkline(values, {
        type: 'line',
        width: '150',
        height: '100',
        lineColor: '#0ca5e7',
        fillColor: '#e5f3f9'});
      $('#company_query').bind('sparklineRegionChange', function(ev){
        console.log(ev.sparklines[0].getCurrentRegionFields());
        var sparkline = ev.sparklines[0],
            region = sparkline.getCurrentRegionFields(),
            value = region.y;
          var tmp = $("#show_detail");
          var x,y;
          x = $("#company_query").offset().left;
          y = $("#company_query").offset().top;
          $(tmp).css("left",x+"px");
          $(tmp).css("top",y+"px");
          $(tmp).fadeIn(100);
          $(tmp).children("label").html(names[region.x]+" : "+value);

      }).bind('mouseleave', function(){
        var tmp = $("#show_detail");
        $(tmp).css("display","none");
      });
      $('#company_count').html("共有 "+company_count+" 家公司");
}

function job_spark_line(msg){
  // 信息来源-公司数量统计
      var job_query = msg.job_query;
      var job_count = msg.job_count;
      var values = new Array();
      var names = new Array();
      $.each(job_query, function(n,value){
         names.push(value.from_web);
         values.push(value.count);
      });
      $("#job_query").sparkline(values, {
        type: 'line',
        width: '150',
        height: '100',
        lineColor: '#0ca5e7',
        fillColor: '#e5f3f9'});
      $('#job_query').bind('sparklineRegionChange', function(ev){
        var sparkline = ev.sparklines[0],
            region = sparkline.getCurrentRegionFields(),
            value = region.y;
          var tmp = $("#show_detail");
          var x,y;
          x = $("#job_query").offset().left;
          y = $("#job_query").offset().top;
          $(tmp).css("left",x+"px");
          $(tmp).css("top",y+"px");
          $(tmp).fadeIn(100);
          $(tmp).children("label").html(names[region.x]+" : "+value);
      }).bind('mouseleave', function(){
        var tmp = $("#show_detail");
        $(tmp).css("display","none");
      });
      $('#job_count').html("共有 "+job_count+" 个职位");
}
