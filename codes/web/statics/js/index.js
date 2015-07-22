$(document).ready(function(){
    $("#wb-manager").click(function(){
        $(".content").attr("src","menu/manager.html");
    });
    
    $("#command-test").click(function(){
        $(".content").attr("src","menu/command.html");
    });
    
    $("#statistics").click(function(){
        $(".content").attr("src","menu/statistics.html");
    });
}); 