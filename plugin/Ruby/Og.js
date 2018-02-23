
var app = angular.module('demoApp', []);
console.log("Lvl 0");

/*d3.select("#export").on("click", function(){
            //var x = "{toolName : sss}";
            var sw = JSON.stringify({"toolName" : "sss"});
            d3.request("http://192.168.0.2:500/postmethod")
            .send("POST", sw);
        });*/



app.controller('demoController', function($scope) {
$scope.tname= "Search by Tool Name";
$scope.ttype= "Search by Tool Type";

$scope.demoController = function($scope, $http) {
    console.log("lvl 1");
        $scope.update = $scope.tname;
        $http.post("/http://192.168.0.2:500/postmethod/sw", {
            tool : $scope.tname
        })
            event.preventDefault();
}
});


