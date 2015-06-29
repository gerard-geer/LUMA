// LUMA Copyright (c) Gerard Geer 2014-2015 

/*
	The QueryController. Handles functionality regarding
	the querying of the light server for valid light instances.
*/
angular.module('LUMAClient').controller('QueryController', 
[ '$scope', 'LUMAServerService', 'LUMAStateService', 
function($scope, LUMAServerService,LUMAStateService){
	
	// Bind the state service to the scope so we can access it in the dom.
	$scope.state = LUMAStateService;
	
	// The submission callback for the query form.
	this.onSubmit = function(){
				
		// Well we submitted it didn't we?
		LUMAStateService.submitted = true;
		
		// If we're trying to submit a query, we aren't editing a light.
		LUMAStateService.isEditing = false;
		
		// We don't know if we've struck out before we play the game.
		LUMAStateService.noResults = false;
		
		// Clear out the existing elements in the query results.
		LUMAStateService.queryResults.length = 0;
		
		// Submit the light query.
		LUMAServerService.submitLightQuery('<uuid>', LUMAStateService.query);
		
		// Decide whether or not we need to display the sadness dialog.
		if(LUMAStateService.queryResults.length == 0)
		{
			LUMAStateService.noResults = true;
		}
	};
	
	// A function that is called when the text input recieves focus.
	this.onFocus = function()
	{
		// Simply reset the query.
		LUMAStateService.query = '';
	}
}]);