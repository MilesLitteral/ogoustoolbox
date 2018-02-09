
var app = angular.module('demoApp', []);

app.controller('demoController', function($scope) {
$scope.tname= "Search by Tool Name";
$scope.ttype= "Search by Tool Type";
    	    

$scope.update = function($scope) {
    $scope.update = angular.copy.tool
    }

$scope.changeName = function() {
	var text = {'Name' : $scope.ttype, 'Type' : $scope.tname};
	var obj = JSON.stringify(text);
	var sw = JSON.parse(obj);
	}
});


