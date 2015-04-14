'use strict';
var controllers = angular.module("organicApp.controllers", []);

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
