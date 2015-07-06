'use strict';
var controllers = angular.module("fpgApp.controllers", []);

controllers.controller("ProfileCtrl", ["$scope", "$log" ,"$rootScope", "currentUserService",

  function ($scope, $log, $rootScope, currentUserService) {

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
    "$rootScope","confirmBox","clubService","$stateParams", "$state","AddressService","BookingService",
    function ($scope, resourceService, $log, toastr, $rootScope, confirmBox,clubService,$stateParams,
              $state,AddressService,BookingService) {
    $scope.queryParams = {club:$stateParams.club};
    $scope.objectList = [];

    if(!$stateParams.club)
    {
        $state.go("club")
    }

    $scope.club = $stateParams


    $scope.open = function($event, resource) {
    $event.preventDefault();
    $event.stopPropagation();
    resource.opened = true;

  };


    $scope.loadAddress = function () {
        /**
         * Get list from service and store it in objectList
         */
        return AddressService.list().then(function (response) {
            $scope.AddressList = response;
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

       $scope.loadSlots = function (resource) {
        /**
         * Get list from service and store it in objectList
         */
       resource.slotList = [];
//       resource.filterbooking = {};


       resource.filterbooking.resource = resource
       var request_date =  resource.filterbooking.date
       request_date = (request_date.getMonth()+1) + '/' + request_date.getDate()+ '/' + request_date.getFullYear()

       var date_ot = new Date(request_date + ", " + resource.open_time)
       var open_time = date_ot.getTime()
       var date_ct = new Date(request_date + ", " + resource.close_time)
       var close_time = date_ct.getTime()

          BookingService.list({"date":request_date, "resource":resource.id}).then(function (response) {
          $scope.bookingList = response;

        for(var i = open_time; i < close_time; i+=3600000)
        {
            var st_time_date = new Date(i);
            var start_time = st_time_date.toTimeString().split(" ")[0]

            var end_date_time = new Date(i+3600000);
            var end_time = end_date_time.toTimeString().split(" ")[0]

            var dict = {
                "start_time": start_time,
                "end_time": end_time,
                "isBooked": false
            }

            for (var j = 0; j < $scope.bookingList.length; j++)
            {
                if($scope.bookingList[j].start_time == start_time && $scope.bookingList[j].end_time == end_time )
                {
                     dict.isBooked = true;
                }
            }

            resource.slotList.push(dict)

        }

        });

    };

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

   $scope.loadData = function () {
        /**
         * Get list from service and store it in objectList
         */
       return resourceService.list($scope.filterform).then(function (response) {
           $scope.objectList = response;
           productService.addProduct($scope.objectList, $scope.filterform)

           $location.url('result')
        });

    };

}]);


controllers.controller("searchCtrl", ["$scope", "$log", "$rootScope", "$state", "AddressService", "SportService",
    "resourceService", "productService","BookingService","$modal","SETTINGS","toastr","$window",
    function ($scope, $log, $rootScope, $state, AddressService, SportService, resourceService, productService,
              BookingService, $modal, SETTINGS, toastr,$window) {

    $scope.filterform = {};
    $scope.AddressList = [];
    $scope.SportList = [];
    $scope.objectList = [];
    $scope.bookingList = [];

        $scope.open = function($event) {
        $event.preventDefault();
        $event.stopPropagation();

        $scope.opened = true;
      };

        $scope.open1 = function($event, resource) {
        $event.preventDefault();
        $event.stopPropagation();
        resource.opened1 = true;

      };
    $scope.filterform = productService.getFilter();
    $scope.objectList = productService.getProducts();

    $scope.loadAddress = function () {
        /**
         * Get list from service and store it in AddressList
         */
        return AddressService.list().then(function (response) {
            $scope.AddressList = response;
        });
    };

    $scope.loadSports = function () {
        /**
         * Get list from service and store it in SportList
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

       return resourceService.list($scope.filterform).then(function (response) {
       $scope.objectList = response;

        });
    };

      $scope.loadSlots = function (resource) {
        /**
         * Get list from service and store it in objectList
         */
       resource.slotList = [];

       resource.filterbooking.resource = resource
       var request_date =  resource.filterbooking.date
       request_date = (request_date.getMonth()+1) + '/' + request_date.getDate()+ '/' + request_date.getFullYear()

       var date_ot = new Date(request_date + ", " + resource.open_time)
       var open_time = date_ot.getTime()
       var date_ct = new Date(request_date + ", " + resource.close_time)
       var close_time = date_ct.getTime()

          BookingService.list({"date":request_date, "resource":resource.id}).then(function (response) {
          $scope.bookingList = response;

        // This loop will create slots according to the open-time and close-time of resources
        for(var i = open_time; i < close_time; i+=3600000)
        {
            var st_time_date = new Date(i);
            var start_time = st_time_date.toTimeString().split(" ")[0]

            var end_date_time = new Date(i+3600000);
            var end_time = end_date_time.toTimeString().split(" ")[0]

            var dict = {
                "start_time": start_time,
                "end_time": end_time,
                "isBooked": false
            }
            // This loop will check whether booking entry is made in the database and set isBooked flag accordingly
            for (var j = 0; j < $scope.bookingList.length; j++)
            {
                if($scope.bookingList[j].start_time == start_time && $scope.bookingList[j].end_time == end_time )
                {
                     dict.isBooked = true;
                }
            }

            resource.slotList.push(dict)

        }

        });

    };


        $scope.slotModelBox = function (slot, resource) {
            if(slot.isBooked)
            {
                toastr.error("Slot already boooked.");
                return;
            }
            var modalInstance = $modal.open({
                templateUrl: SETTINGS.TEMPLATE_DIR + 'slot-result.html',
                controller: slotCtrl,
                size: "sm",
                resolve: {
                    resource: function () {
                        return resource;
                    },
                    slot: function() {
                        return slot;
                    }

                }

            });
            modalInstance.result.then(function(){
                $scope.loadSlots(resource);
            })
        };

}]);

function slotCtrl($scope, $rootScope, resource, slot, BookingService, toastr, $modalInstance,$cookies,$window){

    $window.Stripe.setPublishableKey('pk_test_y5oUXrezhpsYQ4apkZwAO0F4');
    $scope.CSRF = $cookies['csrftoken']
    $scope.stripeCallback = function (code, result) {
        if (result.error) {
            window.alert('it failed! error: ' + result.error.message);
        } else {
            $scope.save(result.id)
        }
    };

    $scope.save = function(token){
            var newBooking = {
                "user": $rootScope.currentUser.id,
                "date": resource.filterbooking.date,
                "start_time": slot.start_time,
                "end_time" : slot.end_time,
                "resource": resource.id,
                "token": token,
                "fee": resource.fee
            }
            BookingService.save(newBooking).then(function (response) {
                angular.copy(response, newBooking);
                toastr.success('Booked Successfully');
                $modalInstance.close("close");
            })
        }
}
