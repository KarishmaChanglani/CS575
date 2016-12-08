'use strict';

var loginModule = angular.module('LoginModule', []);
loginModule.controller('LoginController', ['$scope', '$rootScope', '$location', 'AuthenticationService',
        function ($scope, $rootScope, $location, AuthenticationService) {
            // reset login status
            AuthenticationService.ClearCredentials();

            $scope.login = function () {
                $scope.dataLoading = true;
                AuthenticationService.Login($scope.username, $scope.password, function(response) {
                    if(response.status === 'success') {
                        console.log(response.id);
                        AuthenticationService.SetCredentials(response.id);
                        $location.path('/dashboard');
                    } else {
                        $scope.error = response.message;
                        $scope.dataLoading = false;
                    }
                });
            };
        }]);