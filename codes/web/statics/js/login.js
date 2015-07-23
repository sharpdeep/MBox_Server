function getCookie(name){
	var x = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return x ? x[1]:undefined;
}

$(document).ready(function(){
	$("#login").click(function(){
		var user = $("#username").val();
		var pwd = $("#password").val();
        $.ajax({
			type:"POST",
			url:"/login",
			data:{"username":user,"password":hex_md5(pwd)},
			cache:false,
			success:function(data){
				if(data == '00'){
				    alert("User does't exist");
				}
				else if(data == '10'){
				    alert("password error");
				}
				else{
				    window.location.href='/'+user;
				}
			},
			error:function(){
				alert("error!");
			},
		});
	});
});