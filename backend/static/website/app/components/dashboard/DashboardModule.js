var dashboardModule = angular.module('DashboardModule', ['counter', 'chart.js']);

dashboardModule.controller('DashboardController', function ($scope, $http) {
    $scope.totalUsers = 0;
    var parameters = {user: '1', password : 'password'};

});
dashboardModule.controller("IpCtrl", function ($scope, $http) {
    var parameter = {user: '1', category:'ip', start:0, count:10};
    $http.post("http://127.0.0.1:5678/user/data/", parameter).success(function(data){
        console.log(data.records);
        $scope.records = data.records;
    })
});
