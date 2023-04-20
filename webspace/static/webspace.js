app.controller('WebSpaceController',
     ['$scope', '$rootScope', function($scope, $rootScope){
 
 
         $scope.alert = function(x){
             alert(x);
         };
 
         $scope.click_create = function(){

          event = new Event("formsubmit");
          if ($("create_webspace_form")[0].dispatchEvent(event)){ 

            site_name = $("#site_name").val();
            admin_email = $("#admin_email").val();
            admin_password = $("#admin_password").val();

            $.ajax({type:"POST", url: "create_webspace", data: { site_name : skill, admin_email : admin_email, admin_password : admin_password }, success: function(data){
            obj = $.parseJSON(data)
            $.each(obj, function(key, val){
              $("#create_result").append('<p>' + val + '</p>');
            });
            }});
           }
          };
          

    }]);


(function() {
  'use strict';
  window.addEventListener('load', function() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('formsubmit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();
