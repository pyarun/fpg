'use strict';
var services = angular.module("fpgApp.services", []);

/*Provides information of current logged in user*/

services.service("currentUserService", ["Restangular", "$log", "$q", "$cookies",
  function (Restangular, $log, $q, $cookies) {
    var _user = $q.defer();
    var _key=null;
    var user = null;
    var _is_authenticated=null;

    function getUser(){
      Restangular.one("me").get().then(function (response) {
        _user.resolve(response);
        user = response;
        user.is_authenticated=true;
      });
      return _user.promise;
    }



    return {
      "getKey": function(){
        return _key;
      },
      "setKey": function(key){
        _key=key;
      },
      "getUser": function () {
        return user;
      },
      "promise": getUser,
      "update": function (euser) {
        var temp = euser.save({}, {
          "X-CSRFToken": $cookies['csrftoken']
        });
        temp.then(function (response) {
          user = response;
        });
        return temp;
      },
      "save": function (item) {
        return item.save({}, {
          "X-CSRFToken": $cookies['csrftoken']
        });
      }
    };

  }]);


/*generic confirm box
 * Useage: confirmBox.pop(callbackfunction);
 * */
//services.service("confirmBox", ["SETTINGS", "$modal",
//  function (SETTINGS, $modal) {
//    return {
//      pop: function (callback) {
//        $modal.open({
//                      templateUrl: SETTINGS.TEMPLATE_DIR + 'confirm-modal.html',
//                      controller: ["$scope", "$modalInstance", "okFunc",
//                        function ($scope, $modalInstance, okFunc) {
//
//                          $scope.action = function () {
//                            $modalInstance.close("ok");
//                            okFunc();
//                          };
//                          $scope.cancel = function () {
//                            $modalInstance.dismiss('cancel');
//                          };
//
//                        }],
//                      size: "sm",
//                      resolve: {
//                        okFunc: function () {
//                          return callback;
//                        }
//                      }
//                    });
//
//      }
//    };
//  }]);