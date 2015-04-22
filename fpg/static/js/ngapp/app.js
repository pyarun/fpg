'use strict';
//starting point of angular application
// all the angular configurations will be maintained here
var organicApp = angular.module("fpgApp", ["ui.router", "ui.bootstrap", "restangular", "ngCookies", "toastr",
   "ng.django.urls",
    "fpgApp.controllers", 'fpgApp.services'
]);

organicApp.constant("SETTINGS", {
  "STATIC_URL": djsettings.STATIC_URL,
  "TEMPLATE_DIR": djsettings.STATIC_URL + 'js/ngapp/tmplts/'
});

organicApp.config(["$stateProvider", "$urlRouterProvider", "SETTINGS", "RestangularProvider", "toastrConfig",
    "$httpProvider",
    function ($stateProvider, $urlRouterProvider, SETTINGS, RestangularProvider, toastrConfig,
        $httpProvider) {

      $urlRouterProvider.otherwise('home');

      RestangularProvider.setBaseUrl('/api/v1');
      RestangularProvider.setRequestSuffix("/");

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
        positionClass: 'toast-position'
      });


      //Routes
      $stateProvider.state('home', {
        url: '/home',
        templateUrl: function ($stateParams) {
          return SETTINGS.TEMPLATE_DIR + 'home.html';
        }
      }).state('login', {
        url: '/login',
        templateUrl: function ($stateParams) {
          return SETTINGS.TEMPLATE_DIR + 'auth/login.html';
        },
        controller: "LoginCtrl"
      }).state('register', {
        url: '/register',
        templateUrl: function ($stateParams) {
          return SETTINGS.TEMPLATE_DIR + 'auth/register.html';
        }
      }).state('forgot_password', {
        url: '/forgot_password',
        templateUrl: function ($stateParams) {
          return SETTINGS.TEMPLATE_DIR + 'auth/forgot_password.html';
        }
      }).state('reset_password', {
        url: '/reset_password',
        templateUrl: function ($stateParams) {
          return SETTINGS.TEMPLATE_DIR + 'auth/reset_password.html';
        }
      });

}]);





organicApp.run(["$rootScope", "SETTINGS", function ($rootScope, SETTINGS) {
  //Add settings in $rootScope so that they can be directly accessed in HTML
  $rootScope.SETTINGS = SETTINGS;
}]);
