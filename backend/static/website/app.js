'use strict';

var mainApp = angular.module('MainApp', ['ngRoute', 'ngResource', 'angular-loading-bar', 'DashboardModule', 'UserModule']);
mainApp.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.
        when('/dashboard', {
            // Dashboard Module
            templateUrl : "app/components/dashboard/Dashboard.html",
            controller : 'DashboardController'
        }).
        when('/users', {
            // User Module
            templateUrl : 'app/components/user/User.html',
            controller : 'UserController'
        }).
        otherwise({
            redirectTo : '/dashboard'
        });
}]);

mainApp.filter('dateInMillis', function() {
    return function(dateString) {
        return Date.parse(dateString);
    };
});