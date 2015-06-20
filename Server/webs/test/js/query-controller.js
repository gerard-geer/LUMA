/*
	The QueryController. Handles functionality regarding
	the querying of the light server for valid light instances.
*/
angular.module('LumaClient').controller('QueryController', ['$animate', '$rootScope', function($animate, $rootScope){
	// The query that will be sent to the server.
	this.query = null;
	// Our fake response from the server.
	this.response = new Array();
	// Whether or not this query has been submitted.
	this.submitted = false;
	// Whether or not we need to display the sadness dialog.
	this.noResults = false;
	// Whether or not there is a light to edit.
	this.isEditing = false;
	// The submission callback for the query form.
	this.onSubmit = function(){
		
		// Well we submitted it didn't we?
		this.submitted = true;
		// If we're trying to submit a query, we aren't editing a light.
		
		$rootScope.isEditing = false;
		// We don't know if we've struck out before we play the game.
		this.noResults = false;
		
		this.response = Array();
		lowercase = this.query.toLowerCase(); // For better comparison.
		for(var i = 0; i < testLights.length; ++i)
		{
			if(	testLights[i].name.toLowerCase().indexOf(lowercase) >= 0 ||
			testLights[i].client.toLowerCase().indexOf(lowercase) >= 0 )
				this.response.push(testLights[i]);
		}
		if(this.response.length == 0)
		{
			this.noResults = true;
		}
	};
}]);