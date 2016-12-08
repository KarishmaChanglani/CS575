'use strict';

var machineModule = angular.module('MachineModule', []);

machineModule.controller('MachineController', function ($rootScope, $scope, $routeParams, AppService) {
    $scope.machineId = $routeParams.machineId;
    var parameters = {
        machine: $scope.machineId,
        user: $rootScope.globals.currentUser.userId,
        start:0,
        count:100,
        category: 'ip'
    };
    AppService.Machines(parameters).
    then(function (response) {
        $scope.records = response.data.records;
    }, function (error) {});
});