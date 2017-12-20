(function($){
    var validate = function(){
        $("#register_info_form").validate({
            rules:{
                username: {
                    required:true,
                    regex: /\w{6,16}/

                },
                password: {
                    required:true,
                    regex: /\w{6,16}/
                },
                password2: {
                    equalTo:'#password'
                },
                email:{
                    required:true,
                    email:true
                },
                companyName:{
                    required:true
                }
            }
        });
    };
    var bindUserInfoForm = function() {

        var userInfoModel = kendo.observable({
            username : '',
            password : '',
            password2 : '',
            email : '',
            contactPhone : '',
            companyName:'',
            regist: function(e){

                var userInfo = this.toJSON();

                if( !$("#register_info_form").valid()){
                    return;
                }
                nb.rpc.userApi.c("registerUser",{userInfo:userInfo})
                .success(function(msg){
                    alert(msg);
                });

            }
        });

        kendo.bind($("#register_info_div"), userInfoModel);

    }

    $(document).ready(function(){
        validate();
        bindUserInfoForm();

    });
})(jQuery);
