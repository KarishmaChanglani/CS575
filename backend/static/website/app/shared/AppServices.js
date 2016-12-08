'use strict';

var appServices = angular.module('AppServices', []);

appServices.factory('AppService', function ($rootScope, $http) {
    var service = {};

    service.Users = function (parameters) {
        return $http.post('/user/data/split/', parameters);
    };
    service.Machines = function (parameters) {
        return $http.post('/machine/data/', parameters);
    };

    return service;
});

appServices.factory('AuthenticationService', function ($rootScope, $http, $cookieStore) {

    var service = {};
    service.Login = function (username, password, callback){
        $http.post('/user/', {user: username, password: password}).
            success(function (response) {
                callback(response);
        });
    };

    service.SetCredentials = function (userId) {

        $rootScope.globals = {
            currentUser: {
                userId: userId
            }
        };
        $cookieStore.put('globals', $rootScope.globals);
    };

    service.ClearCredentials = function () {
        $rootScope.globals = {};
        $cookieStore.remove('globals');
    };

    return service;
});