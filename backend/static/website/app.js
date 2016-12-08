'use strict';

var mainApp = angular.module('MainApp',
    ['ngRoute', 'ngResource', 'ngCookies', 'angular-loading-bar', 'LoginModule','DashboardModule', 'MachineModule', 'AppServices']);
mainApp.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.
        when('/login', {
            controller: 'LoginController',
            templateUrl: 'app/components/login/Login.html',
        })
        .when('/dashboard', {
            // Dashboard Module
            templateUrl : "app/components/dashboard/Dashboard.html",
            controller : 'DashboardController'
        })
        .when('/machine/:machineId', {
            // Machines Module
            templateUrl : 'app/components/machine/Machine.html',
            controller : 'MachineController'
        })
        .otherwise({ redirectTo: '/login' });
}]);

mainApp.run(['$rootScope', '$location', '$cookieStore',
    function ($rootScope, $location, $cookieStore) {
        // keep machine logged in after page refresh
        $rootScope.globals = $cookieStore.get('globals') || {};

        $rootScope.$on('$locationChangeStart', function (event, next, current) {
            // redirect to login page if not logged in
            if ($location.path() !== '/login' && !$rootScope.globals.currentUser) {
                $location.path('/login');
            }
        });
}]);

mainApp.controller('HeaderController', function ($scope, AuthenticationService){
    $scope.logout = function () {
        AuthenticationService.ClearCredentials();
    }
});

mainApp.filter('dateInMillis', function() {
    return function(dateString) {
        return Date.parse(dateString);
    };
});