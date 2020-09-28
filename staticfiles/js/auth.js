$(document).ready(function(){
    $('#login-form #msg-btn').on('click', function(event){
        $('#login-form #alert-div').removeClass('active');
    });

    $('#signup-form #msg-btn').on('click', function(event){
        $('#signup-form #alert-div').removeClass('active');
    });

    //this method validates login
    function validate_login(e)
    {
        // e.preventDefault();
        if($('#login-form #email').val()===''){
            // e.preventDefault();
            $('#login-form #msg-btn').html('<i class="fa fa-warning (alias)"></i> Email is required! &times');
            $('#login-form #alert-div').addClass('active');
            return false;       
        } 

        if($('#login-form #password').val()===''){
            // e.preventDefault();
            $('#login-form #msg-btn').html('<i class="fa fa-warning (alias)"></i> Password is required! &times');
            $('#login-form #alert-div').addClass('active');
            return false;       
        }

        if($('#login-form #email').val()==='' || $('#password').val()===''){
            // e.preventDefault();
            $('#login-form #msg-btn').html('<i class="fa fa-warning (alias)"></i> Please all field are required&times');
            $('#login-form #alert-div').addClass('active');
            return false;    
        }
        return true;
    }

    //this method validates login
    function validate_register(e)
    {
        if($('#signup_name').val()===''){
            // e.preventDefault();
            $('#signup-form #msg-btn').html('<i class="fa fa-warning (alias)"></i>Name is required! &times');
            $('#signup-form #alert-div').addClass('active');
            return false;       
        }

        if($('#signup_email').val()===''){
            // e.preventDefault();
            $('#signup-form #msg-btn').html('<i class="fa fa-warning (alias)"></i> Email is required! &times');
            $('#signup-form #alert-div').addClass('active');
            return false;       
        } 

        if($('#signup_password').val()===''){
            // e.preventDefault();
            $('#signup-form #msg-btn').html('<i class="fa fa-warning (alias)"></i> Password is required! &times');
            $('#signup-form #alert-div').addClass('active');
            return false;       
        }

        if($('#signup_cfm_password').val()===''){
            // e.preventDefault();
            $('#signup-form #msg-btn').html('<i class="fa fa-warning (alias)"></i> Confirm Password is required! &times');
            $('#signup-form #alert-div').addClass('active');
            return false;       
        }

        if($('#signup_cfm_password').val()!=='' && $('#signup_password').val() !==''){
            if($('#signup_cfm_password').val() !== $('#signup_password').val()){
                // e.preventDefault();
                $('#signup-form #msg-btn').html('<i class="fa fa-warning (alias)"></i> Confirm Password is incorrect!&times');
                $('#signup-form #alert-div').addClass('active');
                return false;
            }
        }
        return true;
    }



    $('#msg-btn').on('click', function(event){
        $('#alert-div').removeClass('active');
    });

    $("#login-form button[type='submit']").on('click', function(event){
        event.preventDefault();
        if (validate_login(event)){
            var email = $("#login-form input[name='email']").val();
            var password = $("#login-form input[name='password']").val();
            $("#login-form #login-btn").attr('disabled', 'disabled');
            $("#login-form #login-btn .loader").css('display', 'block');
            $.ajax({
                
                url: '/ajax_login/',
                method: 'POST',
                data: {
                    email: email/*'admin'*/,
                    password: password/*'!@#$qwer'*/,
                    csrfmiddlewaretoken:$('#login-form input[name=csrfmiddlewaretoken]').val(),
                },
                success:function(response){
                    if(response.success == true){
                        if(response.order == true){
                            window.location.href = "/ownguestmapp/"
                        }
                        else{
                            window.location.href = "/planprices/"
                        }
                    }
                    else{
                        $('#login-form #msg-btn').html(response.message + '&times');
                        $('#login-form #alert-div').addClass('active');
                    }
                    $("#login-form #login-btn .loader").css('display', 'none');
                    $("#login-form #login-btn").removeAttr('disabled');
                },
            });
        } 
    });


    $("#modal_form_signup button[type='submit']").on('click', function(event){
        event.preventDefault(event);
        if(validate_register(event)){
            var name = $("input[name='signup_name']").val();
            var email = $("input[name='signup_email']").val();
            var password = $("input[name='signup_password']").val();
            console.log(name);
            console.log(email);
            console.log(password);
            $("#signup-form #signup-btn").attr('disabled', 'disabled');
            $("#signup-form #signup-btn .loader").css('display', 'block');
            $.ajax({
                url: '/ajax_register/',
                method: 'POST',
                data: {
                    username: name,
                    email: email,
                    password: password,
                    csrfmiddlewaretoken:$('#signup-form input[name=csrfmiddlewaretoken]').val(),
                },

                success:function(response){
                    if(response.success == true){
                        $('#modal_form_signup').modal('hide');
                        $("#modal_form").modal('show');
                        $("#login-form #email").val(email);
                        $("#login-form #password").val(password);
                    } else {
                        $('#signup-form #msg-btn').html(response.message + '&times');
                        $('#signup-form #alert-div').addClass('active');
                    }
                    $("#signup-form #signup-btn .loader").css('display', 'none');
                }
            });
        }
    });
})
