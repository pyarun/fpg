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


services.service('farmService', ['Restangular', '$cookies', function (Restangular, $cookies) {
  var _db = Restangular.service("farms");
  Restangular.extendModel('farms', function (model) {
    model.getFullAddress = function () {
      return ( model.farm_address.line1 + ' ' + model.farm_address.line2
          + model.farm_address.area + ', ' + model.farm_address.city
          + model.farm_address.state + ', ' + model.farm_address.country + '.' );
    };
    model.edit = false;
    return model;
  });
  return{
    list: function (queryParams) {
      queryParams = queryParams || {};
      return _db.getList(queryParams);
    },
    save: function (item) {
      if (item.id) {
        return item.save({}, {
          "X-CSRFToken": $cookies['csrftoken']
        });
      }
      else {
        return _db.post(item, {}, {
          "X-CSRFToken": $cookies['csrftoken']
        });
      }
    },
    remove: function (item) {
      return item.remove({}, {
        "X-CSRFToken": $cookies['csrftoken']
      });
    }
  }
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