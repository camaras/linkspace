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

        }
    ]);

app.controller('MeetController',
    ['$scope', '$rootScope', function($scope, $rootScope){


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

        $scope.user_click = function($event){

            var domain = "meet.jit.si";
            var options = {
                parentNode: document.querySelector('#meetyou'),
                roomName: $event.target.textContent,
                height: 500 
            }
            $('#dropdown-menu').dropdown('toggle');

	    $scope.skylink.joinRoom($event.target.textContent, {
                audio: true,
                video: true
            }, function(error, success) {
                if (error) return;
                console.log("User connected to " + $event.target.textContent);
	    });

            console.log("value: " + $event.target.textContent);
        };


        $scope.init_host = function(){
            var skylink = new Skylink();

	    $scope.skylink = skylink;

            skylink.on('peerJoined', function(peerId, peerInfo, isSelf){
                if(isSelf) return;
                  var vid = document.createElement('video');
                  vid.autoplay = true;
                  vid.muted = true;
                  vid.id = peerId;
                  document.body.appendChild(vid);
            });


    	    skylink.on('incomingStream', function(peerId, stream, isSelf) {
      		if(isSelf) return;
      		var vid = document.getElementById(peerId);
      	    attachMediaStream(vid, stream);
    	    });

 
    	    skylink.on('peerLeft', function(peerId, peerInfo, isSelf) {
                var vid = document.getElementById(peerId);
		if (vid != null){
                	document.body.removeChild(vid);
		}
            });

    	    skylink.on('mediaAccessSuccess', function(stream) {
                var vid = document.getElementById('myvideo');
                attachMediaStream(vid, stream);
            });

    	    skylink.init({
                apiKey: '6f30e75a-dbe5-438d-b161-58f6967690fd',
                defaultRoom: $rootScope.username
            }, function() {
                 skylink.joinRoom({
                     audio: true,
                     video: true
                 });
            });

            var host_timer = setInterval(function(){
		$.ajax({type:"GET", url: "host"});
	    }, 60000);


        };

        $scope.init_host();

    }]);

app.controller('BookController',
    ['$scope', function($scope){

        }
    ]);
/* end */    
