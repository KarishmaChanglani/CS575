var dashboardModule = angular.module('DashboardModule', ['counter', 'chart.js']);

dashboardModule.controller('DashboardController', function ($rootScope, $scope, $http, AppService) {

    var parameters = {
        user: $rootScope.globals.currentUser.userId,
        category:'ip',
        start:0,
        count:10
    };
    AppService.Users(parameters).
        then(function (response) {
            $scope.records = response.data.records;
    }, function (error) {});

});
