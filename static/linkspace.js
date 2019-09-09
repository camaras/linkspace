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
	service.Register = function(username, password1, password2, email, zoom_meeting_id, callback){

            var formData = new FormData();
            formData.append("username", username);
            formData.append("password1", password1);
            formData.append("password2", password2);
            formData.append("email", email);
            formData.append("zoom_meeting_id", zoom_meeting_id);


	    $http({url: '/accounts/register/', headers: {'Content-Type': 'application/x-www-form-urlencoded'}, method: "POST", data: $.param({"username" : username, "password1" : password1, "password2" : password2, "email": email, "zoom_meeting_id": zoom_meeting_id })})
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
                        $rootScope.Zoom_meeting_id = response.data;
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
		AuthenticationService.Register($scope.username, $scope.password1, $scope.password2, $scope.email, $scope.zoom_meeting_id, function(response) {
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

			$scope.setupVidyoClient($event.target.textContent);

            		/* $scope.vidyoConnector.Connect({
      				host: "prod.vidyo.io",
      				token:  "cHJvdmlzaW9uAHVzZXIxQDg4NzM5Yi52aWR5by5pbwA2MzcwNTM0ODk4MAAAYTRiMjRkMTBlOWExNGU3OWFlYWNmMjFkM2RiZjhjYzJjN2UzNmVlNTU1MDA2MjY2ODRhYmUyMGNmNzc0MDYyMmVjYWQ3NDQwZDA4NDEzYjljOWNiZjNlMWUwMjRiMjI1",    
      				displayName: $scope.username,    
      				resourceId: $event.target.textContent,
      				onSuccess: () => {
                                        alert("success");
         				// successful connection
      				},
      				onFailure: (reason) => {
                                        alert(reason);
        				// failed to connect, check reason to find out why
      				},
      				onDisconnected: (reason) => {
        				//  disconnected, this can be user triggered as well as error case
      				}

            		});*/

        };

        $('#dropdown-menu').dropdown('toggle');



        $scope.init_host = function(){
                /*document.addEventListener('vidyoclient:ready', (e) => {
                    $scope.setupVidyoClient(e.detail);
                }); */

		$.ajax({type:"GET", url: "host", success: function( data ){

               		$scope.setupVidyoClient($scope.username);
		}});

        };

        $scope.setupZoomTag = function(username){


        }

        $scope.setupVidyoClient = function(resourceID){
		VC.CreateVidyoConnector({
		  viewId: "myvideo",                            // Div ID where the composited video will be rendered, see VidyoConnector.html
		  viewStyle: "VIDYO_CONNECTORVIEWSTYLE_Default", // Visual style of the composited renderer
		  remoteParticipants: 15,                        // Maximum number of participants
		  logFileFilter: "warning all@VidyoConnector info@VidyoClient",
		  logFileName:"",
		  userData:""
		}).then(function(vidyoConnector) {
		   	$scope.vidyoConnector = vidyoConnector;
			console.log("connecting to room " + resourceID + " as " + $scope.username + " with token " + $scope.token +"END");
			$scope.vidyoConnector.RegisterParticipantEventListener({
				onJoined: function(participant){
					console.log("Participant Joined " + participant.name );

				},
				onLeft: function(participant){
				},
				onDynamicChanged: function(participants){
				},
				onLoudestChanged: function(participant, audioOnly){
				}
			}).then(function(){
				console.log("RegisterParticipantEventListener Success");
			}).catch(function(){
				console.err("RegisterParticipantEventListener Failed");
			});
			console.log("before token dump");
			console.log($scope.token);
            		$scope.vidyoConnector.Connect({
      				host: "prod.vidyo.io",
      				token: $scope.token,    
      				displayName: $scope.username,    
      				resourceId: resourceID,
      				onSuccess: () => {
                                        console.log("Successfull connection");
         				// successful connection
      				},
      				onFailure: (reason) => {
                                        console.log("failed connect due to " + reason);
        				// failed to connect, check reason to find out why
      				},
      				onDisconnected: (reason) => {
                                        console.log("disconnected")
        				//  disconnected, this can be user triggered as well as error case
      				}

            		});
		});



        };

    }]);

app.controller('BookController',
    ['$scope', function($scope){

        }
    ]);

/* end */    
