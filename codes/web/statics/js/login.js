$(document).ready(function(){
    alert('ok');
    $("#submit").click(function(){
        username = $("#username").val();
        password = $("#password").val();
        if(username && password){
            $.ajax({
                type:"post",
                url :"/login",
                data:{"username":username,"password":hex_md5(password)},
            },
            function(data){
                if(data == 'password error'){
                    alert("�������");
                }
                if(data == 'not exist'){
                    alert("�û�������");
                }
            }
            );
        }
    });
});