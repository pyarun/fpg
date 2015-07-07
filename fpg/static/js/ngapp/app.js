'use strict';
//starting point of angular application
// all the angular configurations will be maintained here
var fpg = angular.module("fpgApp", ["ui.router", "ui.bootstrap", "restangular", "ngCookies", "toastr",
  "ng.django.urls", "angularPayments",
   "fpgApp.controllers", 'fpgApp.services'
]);


fpg.constant("SETTINGS", {
 "STATIC_URL": djsettings.STATIC_URL,
 "TEMPLATE_DIR": djsettings.STATIC_URL + 'js/ngapp/tmplts/'
});

fpg.config(["$stateProvider", "$urlRouterProvider", "SETTINGS", "RestangularProvider", "toastrConfig",
   "$httpProvider","$locationProvider",
   function ($stateProvider, $urlRouterProvider, SETTINGS, RestangularProvider, toastrConfig,
       $httpProvider,$locationProvider) {

   $urlRouterProvider.otherwise('home');

   RestangularProvider.setBaseUrl('/api/v1');
   RestangularProvider.setRequestSuffix("/");
   $httpProvider.defaults.xsrfCookieName = 'csrftoken';
   $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

   //As a convention in web applications, Ajax requests shall send the HTTP-Header
     $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

     //Error pages
     $stateProvider.state('page403', {
       url: '/forbidden',
       templateUrl: function ($stateParams) {
         return SETTINGS.TEMPLATE_DIR + 'err/403.html';
       }
     });

     angular.extend(toastrConfig, {
       closeButton: true,
       timeOut: 2000,
       positionClass: 'toast-top-right'
     });


     //Routes
     $stateProvider.state('home', {
       url: '/home',
       templateUrl: function ($stateParams) {
         return SETTINGS.TEMPLATE_DIR + 'home.html';
       },
        controller: "HomeCtrl",
       data:{
         requireLogin:true
       }
      }).state('login', {
        url: '/login',
        templateUrl: function ($stateParams) {
          return SETTINGS.TEMPLATE_DIR + 'auth/login.html';
        },
        controller: "LoginCtrl",
        data:{
          requireLogin:false
        }
      }).state('register', {
        url: '/register',
        templateUrl: function ($stateParams) {
          return SETTINGS.TEMPLATE_DIR + 'auth/register.html';
        },
        controller: "RegisterCtrl",
        data:{
              requireLogin:false
        }
      }).state('forgot_password', {
        url: '/forgot_password',
        templateUrl: function ($stateParams) {
          return SETTINGS.TEMPLATE_DIR + 'auth/forgot_password.html';
        },controller: "passwordCtrl"
      }).state('reset_password', {
        url: '/reset_password',
        templateUrl: function ($stateParams) {
          return SETTINGS.TEMPLATE_DIR + 'auth/reset_password.html';
        }
      }).state('conformation_link', {
       url: '/conformation_link',
       templateUrl: function ($stateParams) {
         return SETTINGS.TEMPLATE_DIR + 'auth/conformation_link.html';
       },
       data:{
         requireLogin:false
       }
      }).state('email_confirm',{
          url:'/email_confirm'
      }).state('profile', {
        url: '/profile',
        templateUrl: function ($stateParams) {
          return SETTINGS.TEMPLATE_DIR + 'profile.html';
        },
        controller : 'ProfileCtrl',
        data:{
          requireLogin:true
        }
      }).state('club', {
        url: '/club',
        templateUrl: function ($stateParams) {
          return SETTINGS.TEMPLATE_DIR + 'my-clubs.html';
        },
        controller : 'MyClubsCtrl',
        data:{
          requireLogin:true
        }
      }).state('resource', {
        url: '/club:club/resource',
        templateUrl: function ($stateParams) {
          return SETTINGS.TEMPLATE_DIR + 'my-resources.html';

        },
        params: {
         club: null
         },
        controller : 'MyResourcesCtrl',
        data:{
          requireLogin:true
        }
      }).state('result', {
        url: '/result',
        templateUrl: function ($stateParams) {
          return SETTINGS.TEMPLATE_DIR + 'search_results.html';

        },
        controller : 'searchCtrl',
        data:{
          requireLogin:true
        }

      });
}]);


fpg.run(["$rootScope", "SETTINGS", "currentUserService", "$state",
  function ($rootScope, SETTINGS, currentUserService, $state) {
    //Add settings in $rootScope so that they can be directly accessed in HTML
    $rootScope.SETTINGS = SETTINGS;


    $rootScope.$on('$stateChangeStart', function (event, toState, toParams) {
      var requireLogin = toState.data.requireLogin;
      if (requireLogin && typeof $rootScope.currentUser === 'undefined') {
        event.preventDefault();
        // get me a login modal!
        currentUserService.promise().then(function (response) {
          console.log(response)
          return $state.go(toState.name, toParams);
        });
      }
    });

  }
]);
