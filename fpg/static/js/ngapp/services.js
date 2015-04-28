'use strict';
var services = angular.module("fpgApp.services", []);

/*Provides information of current logged in user*/

services.service("currentUserService", ["Restangular", "$log", "$q", "$cookies", "$rootScope",
    "$state",
  function (Restangular, $log, $q, $cookies, $rootScope, $state) {
    $log.debug("hellosdfsdfsdf");
    var _user = $q.defer();
    var user = null;

    function getUser(){
      Restangular.one("me").get().then(function (response) { //success
        _user.resolve(response);
        user = response;
        user.is_authenticated=true;
        $rootScope.currentUser = user;
      }, function(response){  //error
        $rootScope.currentUser = undefined;
        $state.go("login");
      });
      return _user.promise;
    }



    return {
      "getKey": function(){
        return user.key;
      },
      "setKey": function(key){
        user.key=key;
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


//services.service("CountryService",['Restangular', '$cookies', function(Restangular, $cookies){
// var url="country/";
// var _db=Restangular.all(url);
// return {
//   list: function(params){
//       params = params || {};
//       return _db.getList(params);
//   }
// };
//}]);


services.service('clubService', ['Restangular', '$cookies', function (Restangular, $cookies) {
    var _db = Restangular.service("club");
    Restangular.extendModel('clubs', function(model){
        model.getFullAddress = function(){
            return (
                model.club_address.state + ', '+ model.club_address.country +'.' );
        };
        model.edit=false;
        return model;
    });
    return{
        list: function (queryParams) {
            queryParams = queryParams || {};
            return _db.getList(queryParams);
        }
    }
}]);
