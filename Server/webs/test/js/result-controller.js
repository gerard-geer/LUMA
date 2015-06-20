/*
	The Result Controller. Handles the functionality of each
	result.
*/
angular.module('LumaClient').controller('ResultController', ['$rootScope', function($rootScope){
	
	this.onSelect = function(light, query){
		// Remove the search results so we can put something else in their
		// place, such as an edit pane.
		query.response = Array();
		console.log("selected light: \n"+light.name+"\n"+light.client);
		lightToEdit = testState;
		$rootScope.isEditing = true;
	};
}]);
