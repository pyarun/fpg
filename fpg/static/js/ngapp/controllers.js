'use strict';
var controllers = angular.module("fpgApp.controllers", []);

controllers.controller("ProfileCtrl", ["$scope", "$log" , "currentUserService", "toastr",

  function ($scope, $log, currentUserService, toastr) {
    currentUserService.promise.then(function (response) {
      $scope.user = response;
    });


    $scope.save = function (object, form) {
      /**
       * Get list from service and store it in objectList
       */
      debugger;
      if (form.$valid) {
        currentUserService.save(object).then(function (response) {
          object.edit = false;
          toastr.success('Saved Successfully');
        }, function () {
          toastr.error('Error while saving.');
        });
      } else {
        form.showFormErrors = true;
        toastr.error('Correct form errors');
      }
    };

  }]);

controllers.controller("LoginCtrl", ["$scope", "$rootScope", "$log", "toastr", "djangoUrl", "$http", "$state",
    "currentUserService","$cookies",
  function($scope, $rootScope, $log, toastr, djangoUrl, $http, $state, currentUserService,$cookies){

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
         toastr.error((response.non_field_errors[0]));
        });

      }else{
        toastr.error("error");
      }


    }

}]);

controllers.controller("passwordCtrl", ["$scope", "$rootScope", "$log", "toastr", "djangoUrl", "$http", "$state",
    "currentUserService","$cookies",
  function($scope, $rootScope, $log, toastr, djangoUrl, $http, $state, currentUserService,$cookies){

    $scope.forget_Password = function(){

      var csrf = $cookies['csrftoken'];
      if($scope.resetForm.$valid){
         var csrf = $cookies['csrftoken'];

         $log.debug($scope.resetModel);
        $http.post(djangoUrl.reverse('rest_password_reset'), $scope.resetModel).success(function(response){



          $state.go("home")

        }).error(function(response){

       toastr.error(response.detail);
        });

      }else{
         alert(_.values(response));
      }


    }

}]);

controllers.controller("RegisterCtrl", ["$scope", "$rootScope", "$log", "toastr", "djangoUrl", "$http", "$state",
    "currentUserService","$cookies",
  function($scope, $rootScope, $log, toastr, djangoUrl, $http, $state, currentUserService,$cookies){

    $scope.register = function(){
      alert("helllo");
      var csrf = $cookies['csrftoken'];
      if($scope.registerForm.$valid){
         var csrf = $cookies['csrftoken'];

         $log.debug($scope.registerModel);
        $http.post(djangoUrl.reverse('rest_register'), $scope.registerModel).success(function(response){


         toastr.success("Email is sent to : "+response.email);


        }).error(function(response){

       toastr.error(response.email[0]);
        });

      }else{
         alert(_.values(response));
      }


    }

}]);