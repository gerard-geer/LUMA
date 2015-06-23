/*
	The QueryController. Handles functionality regarding
	the querying of the light server for valid light instances.
*/
angular.module('LUMAClient').controller('QueryController', 
[ '$scope', 'LUMAServerService', 'LUMAStateService', 
function($scope, LUMAServerService,LUMAStateService){
	// The query that will be sent to the server.
	this.query = "";
	// Whether or not we need to display the sadness dialog.
	// The submission callback for the query form.
	this.onSubmit = function(){
		LUMAStateService.test = 'WE CHANGED IT IN THE QUERY CONTROLLER';
		console.log(LUMAStateService.test);
		// Well we submitted it didn't we?
		LUMAStateService.submitted = true;
		// If we're trying to submit a query, we aren't editing a light.
		LUMAStateService.isEditing = false;
		// We don't know if we've struck out before we play the game.
		LUMAStateService.noResults = false;
		
		LUMAServerService.submitLightQuery('<uuid>', this.query);
		if(LUMAStateService.queryResults.length == 0)
		{
			console.log("WELP NUTTIN");
			LUMAStateService.noResults = true;
		}
	};
}]);