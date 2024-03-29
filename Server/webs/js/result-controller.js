// LUMA Copyright (c) Gerard Geer 2014-2015 

/*
	The Result Controller. Handles the functionality of each
	result.
*/
angular.module('LUMAClient').controller('ResultController', 
['$scope','LUMAServerService','LUMAStateService', 
function($scope, LUMAServerService, LUMAStateService){
	
	// Bind the state service to the controller's scope so that
	// yet again we can access it in the DOM.
	$scope.state = LUMAStateService;
	
	// The on-selection handler. Handles what should be done when
	// the user selects a query result.
	this.onSelect = function(light){
		
		// Store the selected light in the state service.
		LUMAStateService.selectedLight = light;
		
		// Since the query is always displayed in the search
		// bar we change the query to the name of the selected
		// light.
		LUMAStateService.query = LUMAStateService.selectedLight.name;
		
		// Also we clear out all the query results.
		LUMAStateService.queryResults.length = 0;
		
		// We also need to get the state of the light we selected.
		
		// Finally we get the state of the light.
		LUMAServerService.requestLightState('1',
			LUMAStateService.selectedLight);
	};
}]);
