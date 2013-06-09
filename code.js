var user_id="127285"; var user_ten="chienthan1612";var extime="0";
function checktime(){
    if (extime==0){
        retime="Cảm ơn "+user_ten+" đã tin tưởng và và sử dụng tool.<br />Bạn được sử dụng tool vĩnh viễn.";
    }
    else if(extime > 0){
        retime="Cảm ơn "+user_ten+" đã tin tưởng và và sử dụng tool.<br />Bạn còn được sử dụng tool trong <span id=\"countdown\"></span> nữa.";
        var countdowntime=self.setInterval(function(){counttimedown()},1000);
    }
    else{
        retime="Cảm ơn "+user_ten+" đã tin tưởng và và sử dụng tool.<br />Bạn cần hỗ trợ mình để tool tiếp tục hoạt động.";
    }
    $("div#liketool small").html(retime);
}

function counttimedown(){
    
    if(extime<0){
        checktime();
        clearInterval(countdowntime);
    }
    else{
    ngay=parseInt(extime / 86400);
    gio=parseInt((extime%86400)/3600);
    phut=parseInt(((extime%86400)%3600)/60);
    giay=parseInt(((extime%86400)%3600)%60);
    $("div#liketool small span#countdown").html(ngay+" ngày "+gio+" giờ "+phut+" phút "+giay+" giây ");   
    }
    
    
    extime--;
}


function check_rate(){
    $.get("profile.php", function(data) {
        lt_likesmade=data.match(/Likes\sMade<\/label><\/td><td width=\"20\"><\/td><td>(\d+)<\/td><\/tr>/)[1];
        lt_unlike=data.match(/Unlikes \(Reports\)<\/label><\/td><td width=\"20\"><\/td><td>(\d+)<\/td><\/tr>/)[1];
        
        
        $("div#liketool h2 a").append("<br /><br />Rate:"+parseInt(lt_unlike*100/lt_likesmade)+"% - "+parseInt((lt_unlike*100/4)-lt_likesmade));
    });
}

$("body").append("<div style=\"position:fixed;right:20px;bottom:0px;height:418px;width:380px;display:block;background:#fff;border-top:1px solid #000;border-left:1px solid #000;border-right:1px solid #000;border-radius:3px 3px 0px 0px;\" id=\"liketool\"></div>");
$("div#liketool").html("<h2><a href=\"http://hs2t.com/\">Liketool - Hs2T.com</a></h2><small id=\"countdown\" style=\"color:#000;\"></small>");
checktime();
check_rate();






function appendAlert(msg){
    $("div#liketool").append(msg);
}

appendAlert("<br /><b>Start!</b><br />");
appendAlert("Total: "+$("div center iframe").size()+" likes");
var count=0;

function setLike(){
    src=$("div center iframe").eq(count).attr("src");
    srcarr=src.match(/=([^&]+)/g);    
    src="http://likesasap.com/likedonbuttonasap.php?userid="+user_id+"&siteid"+srcarr[2]+"&ownerid"+srcarr[1];
    $("div center iframe").eq(count).attr("src", src);
    count++;
    appendAlert("<br />Like "+count+" Ok");
    if(count>=$("div center iframe").size()){
       setTimeout(function () {  window.location = "http://likesasap.com/fbstdlikes.php"; }, 5000);
    }
}

$(document).ready(function(){
    
    
if($("div center iframe").size()>0){
    
for(i=0;i<$("div center iframe").size();i++){
    setTimeout(function () { setLike();  }, i*2000);
}

}

else{
     setTimeout(function () { window.location = "http://likesasap.com/fbpost.php"; }, 5000);
}



});
