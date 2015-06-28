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

    "currentUserService","$cookies",
  function($scope, $rootScope, $log, toastr, djangoUrl, $http, $state, currentUserService,$cookies){
    $scope.googleLoginLink = djangoUrl.reverse('google_login');
    $scope.facebookLoginLink = djangoUrl.reverse('facebook_login');

    $scope.login = function(){
      if($scope.loginForm.$valid){

        $log.debug($scope.loginModel);
        $http.post(djangoUrl.reverse('rest_login'), $scope.loginModel).success(function (response) {
          var key = response.key;

          currentUserService.promise().then(function (response) {
            $rootScope.currentUser=response;
            $rootScope.currentUser.setKey(key);
            $log.info($rootScope.currentUser);
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


          toastr.success(_.values(response));


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
    if($scope.registerForm.$valid){

         $log.debug($scope.registerModel);
         $http.post(djangoUrl.reverse('rest_register'), $scope.registerModel).success(function(response){


         toastr.success("Email is sent to : "+response.email);
         $state.go("conformation_link")
         $scope.reset();

        }).error(function(response){

       toastr.error(response[Object.keys(response)[0]]);
        });

      }else{
         alert(_.values(response));

      }
    }

    $scope.reset = function(){
        $scope.registerModel = {};
    };

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
        $scope.newClubCreated = true
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
    "$rootScope","confirmBox","clubService","$stateParams", "$state","AddressService",
    function ($scope, resourceService, $log, toastr, $rootScope, confirmBox,clubService,$stateParams,$state,AddressService) {
    $scope.queryParams = {club:$stateParams.club};
    $scope.objectList = [];

    if(!$stateParams.club)
    {
        $state.go("club")
    }

    $scope.club = $stateParams



    $scope.loadAddress = function () {
        /**
         * Get list from service and store it in objectList
         */
        return AddressService.list().then(function (response) {
            $scope.AddressList = response;
//            debugger;
            $log.debug($scope.objectList);
        });
    };

    $scope.loadAddress();


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


controllers.controller("HomeCtrl", ["$scope", "$log", "$rootScope", "$state", "AddressService", "SportService",
    "resourceService", "productService","$location", "$window",
    function ($scope, $log, $rootScope, $state, AddressService, SportService, resourceService, productService, $location, $window) {

    $scope.filterform = {};
    $scope.AddressList = [];
    $scope.SportList = [];
    $scope.objectList = [];
    $scope.resource_filter_list = [];
        $scope.open = function($event) {
        $event.preventDefault();
        $event.stopPropagation();

        $scope.opened = true;

      };


    $scope.loadAddress = function () {
        /**
         * Get list from service and store it in objectList
         */
        return AddressService.list().then(function (response) {
            $scope.AddressList = response;
        });
    };

    $scope.loadSports = function () {
        /**
         * Get list from service and store it in objectList
         */
        return SportService.list().then(function (response) {
            $scope.SportList = response;
        });
    };

    $scope.loadAddress();
    $scope.loadSports();

    var min_date = new Date();
    $scope.mindate = min_date.getFullYear() + '-' + (min_date.getMonth()+1) + '-' + min_date.getDate();

        function addDays(theDate, days) {
        return new Date(theDate.getTime() + days*24*60*60*1000);
    }

     var max_date = addDays(new Date(), 30);
     $scope.maxdate =  max_date.getFullYear() + '-' + (max_date.getMonth()+1)  + '-' + max_date.getDate()


   $scope.loadData = function () {
        /**
         * Get list from service and store it in objectList
         */

       var request_date =  $scope.filterform.date
       $scope.filterform.date = (request_date.getMonth()+1) + '/' + request_date.getDate()+ '/' + request_date.getFullYear()

       return resourceService.list($scope.filterform).then(function (response) {
           $scope.objectList = response;
           for(var i = 0; i < $scope.objectList.length; i++)
           {
               productService.addProduct($scope.objectList[i])
           }
//           $window.location.href = "/#/result"
           $location.url('result')
        });

    };

}]);



controllers.controller("searchCtrl", ["$scope", "$log", "$rootScope", "$state", "AddressService", "SportService",
    "resourceService", "productService","BookingService",
    function ($scope, $log, $rootScope, $state, AddressService, SportService, resourceService, productService,
              BookingService) {

    $scope.filterform = {};
    $scope.filterbooking = {};
    $scope.AddressList = [];
    $scope.SportList = [];
    $scope.objectList = [];
    $scope.bookingDateList = [];

        $scope.open = function($event) {
        $event.preventDefault();
        $event.stopPropagation();

        $scope.opened = true;
      };

        $scope.open1 = function($event) {
        $event.preventDefault();
        $event.stopPropagation();

        $scope.opened1 = true;

      };

    $scope.objectList = productService.getProducts();

    $scope.loadAddress = function () {
        /**
         * Get list from service and store it in objectList
         */
        return AddressService.list().then(function (response) {
            $scope.AddressList = response;
        });
    };

    $scope.loadSports = function () {
        /**
         * Get list from service and store it in objectList
         */
        return SportService.list().then(function (response) {
            $scope.SportList = response;
        });
    };

    $scope.loadAddress();
    $scope.loadSports();

    var min_date = new Date();
    $scope.mindate = min_date.getFullYear() + '-' + (min_date.getMonth()+1) + '-' + min_date.getDate();

        function addDays(theDate, days) {
        return new Date(theDate.getTime() + days*24*60*60*1000);
    }

     var max_date = addDays(new Date(), 30);
     $scope.maxdate =  max_date.getFullYear() + '-' + (max_date.getMonth()+1)  + '-' + max_date.getDate()


      $scope.loadData = function () {
        /**
         * Get list from service and store it in objectList
         */

       var request_date =  $scope.filterform.date
       $scope.filterform.date = (request_date.getMonth()+1) + '/' + request_date.getDate()+ '/' + request_date.getFullYear()

       return resourceService.list($scope.filterform).then(function (response) {
          $scope.objectList = response;

        });
    };


      $scope.loadSlots = function (resource) {
        /**
         * Get list from service and store it in objectList
         */

       $scope.filterbooking.resource = resource
       var request_date =  $scope.filterbooking.date
       $scope.filterbooking.date = (request_date.getMonth()+1) + '/' + request_date.getDate()+ '/' + request_date.getFullYear()

       var date_ot = new Date($scope.filterbooking.date + ", " + resource.open_time)
       var open_time = date_ot.getTime()
       var date_ct = new Date($scope.filterbooking.date + ", " + resource.close_time)
       var close_time = date_ct.getTime()

        for(var i = open_time; i < close_time; i+=3600000)
        {
            var orignal_st_time = new Date(i);
            var start_time = orignal_st_time.toTimeString().split(" ")[0]

            var orignal_ed_time = new Date(i+3600000);
            var end_time = orignal_ed_time.toTimeString().split(" ")[0]
            $scope.bookingDateList.push({
                "start_time": start_time,
                "end_time": end_time
            })

        }


       return BookingService.list($scope.filterbooking).then(function (response) {
          $scope.bookingList = response;

        });

    };

}]);
