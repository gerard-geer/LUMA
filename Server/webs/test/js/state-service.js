// LUMA Copyright (c) Gerard Geer 2014-2015 

/*
	The LUMA Editor State Service. This stores what the user selected,
	whether or not they are editing a light, etc.
*/
angular.module('LUMAClient').factory('LUMAStateService', [function()
{
	return {
		// The query sent to the server.
		query: "",
		// The array of query results returned by the server.
		queryResults: new Array(),
		// Whether or not this query has been submitted.
		submitted: false,
		// Whether or not there were no responses to the query.
		noResults: false,
		// The query result object that the user selected.
		selectedLight: null,
		// The state of the light being edited,
		lightState: null,
		// Whether or not a light is being edited.
		isEditing: false,
		test: "asdfasdfstate"
	}
}]);