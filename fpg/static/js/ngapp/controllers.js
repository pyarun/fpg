'use strict';
var controllers = angular.module("fpgApp.controllers", []);

controllers.controller("ProfileCtrl", ["$scope", "$log" ,"$rootScope", "currentUserService",

  function ($scope, $log, $rootScope, currentUserService) {

//    CountryService.list().then(function(response){
//    $scope.countryList = response;
//
//    });

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
  function ($scope, $rootScope, $log, toastr, djangoUrl, $http, $state, currentUserService) {
    $scope.login = function () {

      if ($scope.loginForm.$valid) {

        $log.debug($scope.loginModel);
        $http.post(djangoUrl.reverse('rest_login'), $scope.loginModel).success(function (response) {
          var key = response.key;

          currentUserService.promise().then(function (response) {
//            $rootScope.currentUser=response;
            $rootScope.currentUser.setKey(key);
            $log.info($rootScope.currentUser);
          });

          $state.go("home")

        }).error(function (response) {
          alert(_.values(response));
        });

      } else {
        alert("error");
      }
    }

}]);


controllers.controller("MyClubsCtrl", ["$scope", "clubService", "$log", "toastr","$rootScope","confirmBox",
    function ($scope, clubService, $log, toastr, $rootScope, confirmBox) {
    $scope.queryParams = {owner:$rootScope.currentUser.id};
    $scope.objectList = [];


    $scope.loadData = function () {
        /**
         * Get list from service and store it in objectList
         */
        $scope.newClubCreated = false;
        return clubService.list($scope.queryParams).then(function (response) {
            $scope.objectList = response;
            $log.debug($scope.objectList);
        });
    };

    $scope.save = function(object, form){
        if(form.$valid){
            clubService.save(object).then(function (response) {
                angular.copy(response, object);
                object.edit = false;
                toastr.success('Saved Successfully');
                $scope.newClubCreated = false
            })
        }
        else{
            form.showFormErrors = true;
        }

    }

    $scope.clubRemove = function(club){
        $scope.newClubCreated = false
        $scope.objectList = _.without($scope.objectList, club)

    }

$scope.addClub = function () {
        var newClub= {
            "owner": $rootScope.currentUser.id,
            "name": "new club",
            "description": "",
            "contact_number": "",
            "address": {
                "line1": "",
                "line2": "",
                "area": "",
                "city": "",
                "state": "",
                "country": "",
                "latitude": null,
                "longitude": null
            }
        };
        $scope.objectList.push(newClub);
        newClub.edit = true;
   };

    $scope.remove = function(item){
        confirmBox.pop(function(){
            clubService.remove(item).then(function(){
               $scope.objectList = _.without($scope.objectList, item);
               toastr.success('Deleted')
            },function(){
                toastr.error('Error while deleting.');
            });
        });
    };

    $scope.loadData();
}]);





controllers.controller("MyResourcesCtrl", ["$scope", "resourceService", "$log", "toastr",
    "$rootScope","confirmBox","clubService","$stateParams", "$state",
    function ($scope, resourceService, $log, toastr, $rootScope, confirmBox,clubService,$stateParams,$state) {
    $scope.queryParams = {club:$stateParams.club};
    $scope.objectList = [];

    if(!$stateParams.club)
    {
        $state.go("club")
    }

    $scope.club = $stateParams


    $scope.loadData = function () {
        /**
         * Get list from service and store it in objectList
         */
        $scope.newResourceCreated = false;
        return resourceService.list($scope.queryParams).then(function (response) {
            $scope.objectList = response;
            $log.debug($scope.objectList);
        });
    };

    $scope.resourceRemove = function(club){
    $scope.newClubCreated = false
    $scope.objectList = _.without($scope.objectList, club)
    $scope.newResourceCreated = false;
    }

    $scope.save = function(object, form){
        if(form.$valid){
            resourceService.save(object).then(function (response) {
                angular.copy(response, object);
                object.edit = false;
                $scope.newResourceCreated = false;
                toastr.success('Saved Successfully');
//                $scope.newClubCreated = false
            })
        }
        else{
            form.showFormErrors = true;
        }
    }

    $scope.remove = function(item){
        confirmBox.pop(function(){
            resourceService.remove(item).then(function(){
               $scope.objectList = _.without($scope.objectList, item);
               toastr.success('Deleted')
            },function(){
                toastr.error('Error while deleting.');
            });
        });
    };

    $scope.addResource = function () {
            if($scope.newResourceCreated == false) {
                $scope.newResourceCreated = true;
                var newResource = {
                    "name": "new resource",
                    "description": "",
                    "club": 1,
                    "open_time": "",
                    "close_time": "",
                    "fee": 0,
                    sport: 1,
                    "status": ""
                };
                $scope.objectList.push(newResource);
                newResource.edit = true;
            }
       };

    $scope.loadData();
}]);