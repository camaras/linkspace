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
    .when("/accounts/register/complete", {
      templateUrl : "/accounts/register/complete/"
    })
    .when("/meet/meet", {
      templateUrl : "/meet/meet/"
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
		});
	};
	service.Register = function(username, password1, password2, email, callback){

            var formData = new FormData();
            formData.append("username", username);
            formData.append("password1", password1);
            formData.append("password2", password2);
            formData.append("email", email);	


	    $http({url: '/accounts/register/', headers: {'Content-Type': 'application/x-www-form-urlencoded'}, method: "POST", data: $.param({"username" : username, "password1" : password1, "password2" : password2, "email": email })})
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
	    $scope.login = function(){
	        AuthenticationService.Login($scope.username, $scope.password, function(response) {
	            if(response.status == 200){
                        $rootScope.$broadcast('Login');
		        $location.path('meet/meet');
		    }
	        })
	    }
	    $scope.register = function(){
		AuthenticationService.Register($scope.username, $scope.password1, $scope.password2, $scope.email, function(response) {
                        if (response.statusText == "OK"){
			    $location.path('accounts/register/complete');
		        }
                    }, function(response){
                        if (response.status == 302){
                            $location.path('accounts/register/complete');
                        }
                    }
                )
            };
      	    
	}
    ]);

app.controller('MenuController',
    ['$scope', '$rootScope', '$location', 'AuthenticationService', 
        function($scope, $rootScope, $location, AuthenticationService){
            $rootScope.$on('Login', function(){
                alert("login");
                $scope.login_status = true;
            });
            $rootScope.$on('Logout', function(){
                alert("logout");
                $scope.login_status = false; 
            });

            $scope.logout = function(){
                AuthenticationService.Logout(function(response){
                    if (response.status == 200){
                        // TODO - check if 200 is correct code for succesfull logout 
                        $rootScope.$broadcast('Logout');
                        $location.path('accounts/login/');
                    }; 
            })
            };

        }
    ]);

app.controller('MeetController',
    ['$scope', function($scope){
        $scope.click_host = function(){
            $.ajax({type:"GET", url: "host", success: function( data ){
                debugger;
                var domain = "meet.jit.si";
                var options = {
                    parentNode: document.querySelector('#host_meet'),
                    roomName: "{{ request.user.username }}",
                    height: 500 
                }
                var api = new JitsiMeetExternalAPI(domain, options);
                setInterval(function(){
                    $.ajax({type:"GET", url: "host"});
                }, 60000);
            }}) 

        };
    }]);
