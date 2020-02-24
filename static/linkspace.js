var app = angular.module("lnkspace", ["ngRoute"]);

app.config(function($routeProvider, $locationProvider, $httpProvider){
    $routeProvider
      .when("/", {
      controller: 'LoginController',	
      templateUrl : "/accounts/login/"
    })
    .when("/accounts/logout/", {
      controller : 'LoginController',
      templateUrl : "/accounts/login/"
    })
    .when("/accounts/login/", {
      controller : 'LoginController',
      templateUrl : "/accounts/login/",
    })
    .when("/accounts/register/", {
      controller : 'LoginController',
      templateUrl : "/accounts/register/"
    })
    .when("/accounts/register/complete/", {
      templateUrl : "/accounts/register/complete/"
    })
    .when("/meet/meet", {
      templateUrl : "/meet/meet/"
    })
    .when("/book/book", {
      templateUrl : "/book/book"
    });

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';


    $locationProvider.html5Mode({
	enabled: true,
	requireBase: false
    });
});

app.factory('AuthenticationService',
    ['$http', function($http){
        var service = {}
	service.Login = function(username, password, callback){
	    $http({url: '/login/', method: "POST", data: {"username": username,"password" :  password }})
	        .then(function(response){
		    callback(response);
		}, function(response){
                    callback(response)
                });
	};
	service.Register = function(username, password1, password2, email, zoom_meeting_id, helper, skills, callback){

            var formData = new FormData();
            formData.append("username", username);
            formData.append("password1", password1);
            formData.append("password2", password2);
            formData.append("email", email);
            formData.append("zoom_meeting_id", zoom_meeting_id);
            formData.append("helper", helper);
            formData.append("skills", skills);


	    $http({url: '/accounts/register/', headers: {'Content-Type': 'application/x-www-form-urlencoded'}, method: "POST", data: $.param({"username" : username, "password1" : password1, "password2" : password2, "email": email, "zoom_meeting_id": zoom_meeting_id, "helper": helper, "skills": skills })})
	        .then(function(response){
		    callback(response);
		});
	};

        service.Logout = function(callback){
	    $http({url: '/accounts/logout/', method: "POST" }).then(function(response){
                callback(response);
            });
        };
	return service;
   }]
);

app.controller('LoginController',
    ['$scope', '$rootScope', '$location', 'AuthenticationService',
        function($scope, $rootScope, $location, AuthenticationService){
            $scope.login_failed = false;

	    $scope.login = function(){
	        AuthenticationService.Login($scope.username, $scope.password, function(response) {
	            if(response.status == 200){
                        $rootScope.username = $scope.username;
                        $rootScope.$broadcast('Login');
		        $location.path('meet/meet');
		    }
                    else
                    {
                        $scope.login_failed = true; 

                    } 
	        })
	    }
	    $scope.register = function(){
		AuthenticationService.Register($scope.username, $scope.password1, $scope.password2, $scope.email, $scope.zoom_meeting_id, $scope.helper, $scope.skills,  function(response) {
                        if (response.statusText == "OK"){
			    $location.path('accounts/register/complete/');
		        }
                    }, function(response){
                        if (response.status == 302){
                            $location.path('accounts/register/complete/');
                        }
                    }
                )
            };
      	    
	}
    ]);


app.controller('ModalController',
    ['$scope', '$rootScope', '$http', 
        function($scope, $rootScope, $http){
            $scope.save_failed = false;
            $rootScope.$on('ModalOpen', function (event){
            
	        $http({url: '/accounts/change/', headers: {'Content-Type': 'application/json'}, method: "GET", data: $.param({"email": $scope.email, "zoom_meeting_id": $scope.zoom_meeting_id, "helper": $scope.helper, "skills": $scope.skills })})
	            .then(function(response){
                        if (response.status == 200){
                            $scope.email = response.data.email;
                            $scope.zoom_meeting_id = response.data.zoom_meeting_id;
                            $scope.helper = response.data.helper;
                            $scope.skills = response.data.skills;
                        } else {

                            $scope.email = "";
                            $scope.zoom_meeting_id = "";
                            $scope.helper = "";
                            $scope.skills = "";
                        }
                });
            }); 


            $scope.account = function(){
                var formData = new FormData();
                formData.append("email", $scope.email);
                formData.append("zoom_meeting_id", $scope.zoom_meeting_id);
                formData.append("helper", $scope.helper);
                formData.append("skills", $scope.skills);


	        $http({url: '/accounts/change/', headers: {'Content-Type': 'application/x-www-form-urlencoded'}, method: "POST", data: $.param({"email": $scope.email, "zoom_meeting_id": $scope.zoom_meeting_id, "helper": $scope.helper, "skills": $scope.skills })})
	            .then(function(response){
                        if (response.status == 200){
		            $('#accountModal').modal('hide');
                        } else {
                            $scope.save_failed = true;
                        }
		    })

             };



        }
    ]);

app.controller('MenuController',
    ['$scope', '$rootScope', '$location', 'AuthenticationService', 
        function($scope, $rootScope, $location, AuthenticationService){
            $rootScope.$on('Login', function(){
                $scope.login_status = true;
            });
            $rootScope.$on('Logout', function(){
                $scope.login_status = false; 
            });

            $scope.logout = function(){
                AuthenticationService.Logout(function(response){
                    if (response.status == 200){
                        // TODO - check if 200 is correct code for succesfull logout
                        $rootScope.username = ""; 
                        $rootScope.$broadcast('Logout');
                        $location.path('accounts/login/');
                    }; 
            })
            };

            $scope.my_account = function(){
                $scope.save_failed = true;
                $('#accountModal').modal('show');
                $rootScope.$emit('ModalOpen', {});

            };

            $scope.account = function(){
                alert("test");  
                var formData = new FormData();
                formData.append("email", email);
                formData.append("zoom_meeting_id", zoom_meeting_id);
                formData.append("helper", helper);
                formData.append("skills", skills);


	        $http({url: '/accounts/change/', headers: {'Content-Type': 'application/x-www-form-urlencoded'}, method: "POST", data: $.param({"email": email, "zoom_meeting_id": zoom_meeting_id, "helper": helper, "skills": skills })})
	            .then(function(response){
                        if (response.status == 200){
                            $('#accountModal').modal('hide');
                        } else {
                            $scope.save_failed = true;

 
		        }
                     });
             };



        }
    ]);

 
app.controller('MeetController',
     ['$scope', '$rootScope', function($scope, $rootScope){
 
 
         /* $.ajax({type:"GET", url: "get_hosting_users", data: { skills: ''}, success: function(data){
             obj = $.parseJSON(data)
             $.each(obj, function(key, val){
                     $("#hosts").append('<a class=\"users dropdown-item\" href=\"https://us04web.zoom.us/s/\"' + val.zoom_meeting_id  + ' ng-click=\"user_click()\">' + val.username + '</a>');
                 });
             }}); */
 
 
         $scope.alert = function(x){
             alert(x);
         };
 
         $scope.click_search = function(){
             skill = $("#skill").val();
             $.ajax({type:"GET", url: "get_hosting_users", data: { skill: skill }, success: function(data){
                 obj = $.parseJSON(data)
                 $.each(obj, function(key, val){
                     $("#hosts").append('<a class=\"users dropdown-item\" href=\"https://us04web.zoom.us/s/\"' + val.zoom_meeting_id  + ' ng-click=\"user_click()\">' + val.username + '</a>');
                 });
             }});
         };
 
 
         $scope.click_connect = function(){
             $("#dropdown-menu").empty();
             $.ajax({type:"GET", url: "get_all_hosting_users", success: function(data){
                 obj = $.parseJSON(data)
                 $.each(obj, function(key, val){
                     $("#dropdown-menu").append('<a class=\"users dropdown-item\" href=\"#\"  ng-click=\"user_click()\">' + val.username + '</a>');
                     $("#dropdown-menu").dropdown('toggle');
                 });
             }});
         };
 
 
         $scope.init_host = function(){
                 /*document.addEventListener('vidyoclient:ready', (e) => {
                     $scope.setupVidyoClient(e.detail);
                 }); */
 
 		$.ajax({type:"GET", url: "host", success: function( data ){

               		$scope.setupVidyoClient($scope.username);
		}});

        };


    }]);

app.controller('BookController',
    ['$scope', function($scope){

        }
    ]);

/* end */    
