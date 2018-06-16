var app = angular.module("lnkspace", ["ngRoute"]);

app.config(function($routeProvider, $locationProvider, $httpProvider){
    $routeProvider
      .when("/", {
      controller: 'LoginController',	
      templateUrl : "/accounts/login/"
    })
    .when("/accounts/login/", {
      controller : 'LoginController',
      templateUrl : "/accounts/login/",
    })
    .when("/accounts/register/", {
      templateUrl : "/accounts/register/"
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
        alert("hello2");
	service.Login = function(username, password, callback){
	    alert("hello3" + username);
	    $http({url: '/login/', method: "POST", data: {"username": username,"password" :  password }})
	        .then(function(response){
		    callback(response);
		});
	};
	return service;
   }]
);

app.controller('LoginController',
    ['$scope', '$rootScope', '$location', 'AuthenticationService',
        function($scope, $rootScope, $location, AuthenticationService){
	    alert("hello" + $scope.username);
	    $scope.login = function(){
		alert("hello4");
	        AuthenticationService.Login($scope.username, $scope.password, function(response) {
	            if(response.status == 200){
		        $location.path('meet/meet');
		    }
	        })
	    }
	}
    ]);

