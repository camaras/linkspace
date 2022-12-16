app.controller('WebSpaceController',
     ['$scope', '$rootScope', function($scope, $rootScope){
 
 
         $scope.alert = function(x){
             alert(x);
         };
 
         $scope.click_create = function(){
             site_name = $("#site_name").val();
             admin_email = $("#admin_email").val();
             admin_password = $("#admin_password").val();

             $.ajax({type:"POST", url: "create_webspace", data: { site_name : skill, admin_email : admin_email, admin_password : admin_password }, success: function(data){
                 obj = $.parseJSON(data)
                 $.each(obj, function(key, val){
                     $("#create_result").append('<p>' + val + '</p>');
                 });
             }});
         };

    }]);
