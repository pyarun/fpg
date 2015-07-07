'use strict';
var services = angular.module("fpgApp.services", []);

/*Provides information of current logged in user*/

services.service("currentUserService", ["Restangular", "$log", "$q", "$cookies", "$rootScope",
    "$state",
    function (Restangular, $log, $q, $cookies, $rootScope, $state) {
        var _user = $q.defer();
        var user = undefined;

        Restangular.extendModel('me', function (model) {
            model.is_authenticated = function () {
                return true;
            };
            model.setKey = function (key) {
                model.key = key;
            };

            model.getKey = function () {
                return model.key;
            }
            return model;
        });

        function getUser() {
            Restangular.one("me").get().then(function (response) { //success
                _user.resolve(response);
                user = response;
                $rootScope.currentUser = user;
            }, function (response) {  //error
                $rootScope.currentUser = undefined;
                $state.go("login");
            });
            return _user.promise;
        }


        return {
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


services.service('clubService', ['Restangular', '$cookies', function (Restangular, $cookies) {
    var _db = Restangular.service("club");
    Restangular.extendModel('clubs', function (model) {
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


services.service('resourceService', ['Restangular', '$cookies', function (Restangular, $cookies) {
    var _db = Restangular.service("resource");
    Restangular.extendModel('resources', function (model) {
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


services.service("SportService", ['Restangular', '$cookies', function (Restangular, $cookies) {
    var url = "sport";
    var _db = Restangular.all(url);
    return {
        list: function (params) {
            params = params || {};
            return _db.getList(params);
        }
    };
}]);


services.service("AddressService", ['Restangular', '$cookies', function (Restangular, $cookies) {
    var url = "address";
    var _db = Restangular.all(url);
    return {
        list: function (params) {
            params = params || {};
            return _db.getList(params);
        }
    };
}]);

services.service('productService', function () {
    var productList = [];
    var filterform = {};

    var addProduct = function (newObj, filter) {
        productList = newObj;
        filterform = filter;
    };

    var getProducts = function () {
        return productList;
    };
    var getFilter = function () {
        return filterform;
    };

    return {
        addProduct: addProduct,
        getProducts: getProducts,
        getFilter: getFilter
    };

});


services.service('BookingService', ['Restangular', '$cookies', function (Restangular, $cookies) {
    var _db = Restangular.service("booking");
    Restangular.extendModel('booking', function (model) {
        model.edit = false;
        return model;
    });
    return{
        list: function (queryParams) {
            queryParams = queryParams || {};
            return _db.getList(queryParams);
        },
        save: function (item) {
            item.date = (item.date.getMonth() + 1) + '/' + item.date.getDate() + '/' + item.date.getFullYear()
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
        }

    }
}]);
