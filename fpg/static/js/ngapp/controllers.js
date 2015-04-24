'use strict';
var controllers = angular.module("fpgApp.controllers", []);

controllers.controller("ProfileCtrl", ["$scope", "$log" ,"$rootScope", "currentUserService",

  function ($scope, $log, $rootScope, currentUserService) {

//    debugger;
    $scope.save = function (object, form) {
      /**
       * Get list from service and store it in objectList
       */
      if (form.$valid) {
        currentUserService.save(object).then(function (response) {
          object.edit = false;
          //toastr.success('Saved Successfully');
        }, function () {
          //toastr.error('Error while saving.');
        });
      } else {
        form.showFormErrors = true;
        //toastr.error('Correct form errors');
      }
    };

  }]);

controllers.controller("LoginCtrl", ["$scope", "$rootScope", "$log", "toastr", "djangoUrl", "$http", "$state",
    "currentUserService",
  function($scope, $rootScope, $log, toastr, djangoUrl, $http, $state, currentUserService){
    $scope.login = function(){

      if($scope.loginForm.$valid){

        $log.debug($scope.loginModel);
        $http.post(djangoUrl.reverse('rest_login'), $scope.loginModel).success(function(response){
          currentUserService.setKey(response.key);
          currentUserService.promise().then(function(response){
            $rootScope.currentUser=response;
          });

          $state.go("home")

        }).error(function(response){
          alert(_.values(response));
        });

      }else{
        alert("error");
      }


    }

}]);