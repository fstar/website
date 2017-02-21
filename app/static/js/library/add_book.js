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
var token = $('meta[name=token]').attr('content');
$.ajaxSetup({
     beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("Token", token);
     }
 })

function search_isbn_button(){ // ISBN匹配按钮的事件
  var ISBN = $("input[name='ISBN']").val();
  if (ISBN.length == 10 || ISBN.length == 13){
    search_by_ISBN(ISBN);
  }else{
    alert("请输入正确的ISBN!");
  }
}


function search_by_ISBN(ISBN_code){//根据ISBN请求豆瓣API
  try{
    $.ajax({
       url:"https://api.douban.com/v2/book/isbn/{ISBN}?callback=?".format({ISBN:ISBN_code}),
       async:true,
       contentType: "application/json; charset=utf-8",
       dataType: "json",
       type:"GET",
       success:function(values){
         console.log(values);
         var name = values["title"];
         var author = values["author"].join(",")+" 著/"+values["translator"].join(",")+" 译";
         var classify_list = [];
         $.each(values.tags, function(n,classify){
            classify_list.push(classify.title);
         });
         var classify = classify_list.join(",")
         var publisher = values.publisher;
         var desc = values.summary;
         var id = values['id'];
         var publish_time = values.pubdate;
        //  var ISBN_code = values.isbn10?values.isbn10:values.isbn13;
         $("input[name='name']").val(name);
         $("input[name='author']").val(author);
        //  $("input[name='ISBN']").val(ISBN_code);
         $("input[name='classify']").val(classify);
         $("input[name='other_classify']").val(classify);
         $("input[name='publisher']").val(publisher);
         $("input[name='publish_time']").val(publish_time);
         $("textarea[name='desc']").val(desc);
       },
       error:function(xhr, ajaxOptions, thrownError){
          alert(xhr.status);
          alert(xhr.statusText);
          alert(xhr.responseText);
      }
    });
    return true;
  }catch(err){
    alert('ISBN不存在');
    return false;
  }
}



// 以下是关于摄像头的操作
// 判断是否可以用摄像头
navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia || navigator.oGetUserMedia;
window.URL = window.URL || window.webkitURL || window.mozURL || window.msURL;
if (navigator.getUserMedia){
   $("#use_camera").removeAttr("disabled");
}
function getUserMedia(constraints, success, failure) {
    navigator.getUserMedia(constraints, function(stream) {
        var videoSrc = (window.URL && window.URL.createObjectURL(stream)) || stream;
        window.stream = stream;
        success.apply(null, [videoSrc]);
    }, failure);
}


function initCamera(constraints, video, callback) {
    getUserMedia(constraints, function (src) {
        video.src = src;
        video.addEventListener('loadeddata', function() {
            var attempts = 10;

            function checkVideo() {
                if (attempts > 0) {
                    if (video.videoWidth > 0 && video.videoHeight > 0) {
                        console.log(video.videoWidth + "px x " + video.videoHeight + "px");
                        video.play();
                        callback();
                    } else {
                        // window.setTimeout(checkVideo, 100);
                    }
                } else {
                    callback('Unable to play video stream.');
                }
                attempts--;
            }

            checkVideo();
        }, function(error){
          console.log(error);
        });
    }, function(e) {
        console.log(e);
    });
}

function copyToCanvas(video, ctx) {
    ( function frame() {
        ctx.drawImage(video, 0, 0);
        var barcode = new Barcode(ctx, 800, 600);
        var line = barcode.scan();

        if (line) {
            console.log(line.isbn);
            $("input[name='ISBN']").val(line.isbn);
            barcode.print(line);
            $("#camera_ui").modal('hide');
            return true;

        } else {
            console.log('Sorry, could not find barcode… please try again');
        }
        window.requestAnimationFrame(frame);
    }());
}

function open_camera(){
  $('#camera_ui').modal('show');
}

$('#camera_ui').on('shown.bs.modal', function (e) {
  // do something...
    var constraints = {
                video: {
                    mandatory: {
                        minWidth: 800,
                        minHeight: 600
                    }
                }
            },
            video = document.getElementById('video'),
            canvas = document.getElementById('canvas');


    initCamera(constraints, video, function() {
        canvas.setAttribute('width', 800);
        canvas.setAttribute('height', 600);
        copyToCanvas(video, canvas.getContext('2d'));
    });
})


$('#camera_ui').on('hidden.bs.modal', function (e) {
    window.stream.getVideoTracks()[0].stop();
    video.removeEventListener('loadeddata',function(){return true});
    var isbn_code = $("input[name='ISBN']").val();
    if (isbn_code.length > 0){
      search_by_ISBN(isbn_code)
    }
})
