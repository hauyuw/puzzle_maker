(function() {    
//setting up the AngularJS module for the features of the froyo order, includes dependencies to include the ngAnimate and UI Bootstrap libraries
var app = angular.module('app', ['ngAnimate','ui.bootstrap']);

//main AngularJS controller for the order 
app.controller('MainController', function($scope){
    this.library = [
        {
            image: 'img/img1.png'
        },
        {
            image: 'img/img2.png'
        },
        {
            image: 'img/img3.png'
        },
        {
            image: 'img/img4.png'
        },
        {
            image: 'img/img5.png'
        },
        {
            image: 'img/img6.png'
        },
        {
            image: 'img/img7.png'
        },
        {
            image: 'img/img8.png'
        },
        {
            image: 'img/img9.png'
        },
        {
            image: 'img/img10.png'
        }
    ];
});
    
})();