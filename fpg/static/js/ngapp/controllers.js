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

controllers.controller("MyFarmsCtrl", ["$scope", "farmService", "$log", "confirmBox", "toastr",
  function ($scope, farmService, $log, confirmBox, toastr) {
    $scope.queryParams = {};
    $scope.objectList = [];

    $scope.loadData = function () {
      /**
       * Get list from service and store it in objectList
       */
      return farmService.list($scope.queryParams).then(function (response) {
        $scope.objectList = response;
        $log.debug($scope.objectList);
      });
    };

    $scope.save = function (object, form) {
      /**
       * Get list from service and store it in objectList
       */
      if (form.$valid) {
        farmService.save(object).then(function (response) {
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

    $scope.addNew = function () {
      var newFarm = {
        "user": 1,
        "name": "New Farm",
        "description": "New Farm",
        "contact_number": "",
        "latitude": null,
        "longitude": null,
        "farm_address": {
          "line1": "",
          "line2": "",
          "area": "",
          "city": "",
          "state": "",
          "country": "",
          "edit": true
        }
      }
      $scope.objectList.push(newFarm);
      newFarm.edit = true;
    };

    $scope.remove = function (item) {
      confirmBox.pop(function () {
        farmService.remove(item).then(function () {
          $scope.objectList = _.without($scope.objectList, item);
        }, function () {
          toastr.error('Error while saving.');
        });
      });
    };

    $scope.loadData();
  }]);
