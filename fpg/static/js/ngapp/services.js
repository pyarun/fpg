'use strict';
var services = angular.module("organicApp.services", []);

/*Provides information of current logged in user*/

services.service("currentUserService", ["Restangular", "$log", "$q", "$cookies",
  function (Restangular, $log, $q, $cookies) {

    var _user = $q.defer();
    var user = null;
    var _db = Restangular.one("me").get().then(function (response) {
      _user.resolve(response);
      user = response;
    });

    return {
      "getUser": function () {
        return user;
      },
      "promise": _user.promise,
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
services.service("confirmBox", ["SETTINGS", "$modal",
  function (SETTINGS, $modal) {
    return {
      pop: function (callback) {
        $modal.open({
                      templateUrl: SETTINGS.TEMPLATE_DIR + 'confirm-modal.html',
                      controller: ["$scope", "$modalInstance", "okFunc",
                        function ($scope, $modalInstance, okFunc) {

                          $scope.action = function () {
                            $modalInstance.close("ok");
                            okFunc();
                          };
                          $scope.cancel = function () {
                            $modalInstance.dismiss('cancel');
                          };

                        }],
                      size: "sm",
                      resolve: {
                        okFunc: function () {
                          return callback;
                        }
                      }
                    });

      }
    };
  }]);