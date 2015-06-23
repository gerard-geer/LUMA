/*
	The Result Controller. Handles the functionality of each
	result.
*/
angular.module('LUMAClient').controller('ResultController', 
['$scope','LUMAServerService','LUMAStateService', 
function($scope, LUMAServerService, LUMAStateService){
	
	this.onSelect = function(light){
		LUMAStateService.selectedLight = light;
		console.log("selected light: \n"+LUMAStateService.selectedLight.name+
		"\n"+LUMAStateService.selectedLight.client);
		LUMAStateService.isEditing = true;
	};
}]);
