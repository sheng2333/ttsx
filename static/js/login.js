$(function(){


	var error_name = false;
	var error_password = false;
	var error_yzm = false;




	$('#username').blur(function() {
		check_user_name();
	});

	$('#pwd').blur(function() {
		check_pwd();
	});

	$('#yzm').blur(function() {
		check_yzm();
	});

	function check_user_name(){
		var len = $('#username').val().length;
		if(len<5||len>20)
		{
			$('#username').next().html('请输入5-20个字符的用户名')
			$('#username').next().show();
			error_name = true;

		}
		else
		{
			$('#username').next().hide();
			error_name = false;
		}
	}

	function check_pwd(){

		var len = $('#pwd').val().length;
		if(len<8||len>20)
		{
			$('#pwd').next().html('密码最少8位，最长20位')
			$('#pwd').next().show();
			error_password = true;
		}
		else
		{
				$('#pwd').next().hide();

				error_password = false;
			}
	}

	var yzm_url='/user/yanzhengma?num='
	var num = new Date().getTime()
	$('#yzm_img').click(function () {
		yzm_url+=num
		$('#yzm_img').attr('src',yzm_url)
    })
	function check_yzm(){
		$.get('/user/check_yzm/?yzm='+$('#yzm').val(),function (data) {
				if (data.count==1){
					$('.yzm_error').html('验证码不正确')
					$('.yzm_error').show();
					error_yzm = true;
				}else {
					$('.yzm_error').hide();
					error_yzm = false;
				}
            });

	}



	$('#reg_form').submit(function() {

		check_user_name();
		check_pwd();
		check_yzm()


		if (error_name == false && error_password == false && error_yzm == false)
		{
			return true;
		}
		else
		{
			return false;
		}


	});



})