// LUMA Copyright (c) Gerard Geer 2014-2015 
					
var testState = {	success: true,
					message: "simple message from client of Couch",
					id:"561519e7-f6a8-462b-a749-c7de69ade7d1",
					name: "Couch",
					client: "Max's Room",
					r_t: [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
					r_v: [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
					r_c: 0,
					g_t: [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
					g_v: [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
					g_c: 0,
					b_t: [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
					b_v: [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
					b_c: 0};
					
/*
	The lUMA Server Service. This functions as a singleton that
	encapsulates interactions with the server, and stores the
	selected query result and the state of the requested light.
*/
angular.module('LUMAClient').factory('LUMAServerService', 
['$http', 'LUMAStateService', function($http, LUMAStateService) {
	
	// "Requests a selection of available lights from the server
	// based on a query supplied by the user, and the UUID of that
	// user."
	function performLightQuery(uuid, query)
	{
		// Pre-emptively clear out the Query Result array.
		LUMAStateService.queryResults.length = 0;
		
		// Go ahead and clear out the old light state and errors.
		LUMAStateService.lightState = null;
		LUMAStateService.isEditing = false;
		LUMAStateService.errorMessage = '';
		LUMAStateService.isError = false;
		
		// Convert the query to lower-case for better comparison.
		lowercase = query.toLowerCase();
		
		// Create a stringified JSON object as our request.
		request = JSON.stringify({'uuid':uuid,'query':query})
		
		// Send the request!
		$http.get('resources/lights/'+request)
		.success(function(response)
		{
			// Get the lights for ease of use.
			lights = response['lights'];
			
			// Set the interface state's query results to the actual results.
			LUMAStateService.queryResults = 
				LUMAStateService.queryResults.concat(lights)
				
			// If there were no results we want to display the sad dialog.
			LUMAStateService.noResults = (lights.length == 0);
		});
	}
	
	// "Requests from the server the state of the light."
	function performStateQuery(uuid, light)
	{
		// Go ahead and clear out the old light state and errors.
		LUMAStateService.lightState = null;
		LUMAStateService.isEditing = false;
		LUMAStateService.errorMessage = '';
		LUMAStateService.isError = false;
		
		// Stringify our request terms for transmission.
		request = JSON.stringify({'uuid':uuid,'id':light['id']})
		
		// Send the request!
		$http.get('resources/lights/state/'+request)
		.success(function(response)
		{
			console.log(response);
			// If the state query was successful...
			if(response['success'])
			{
				// We set the light state to edit to the response,
				LUMAStateService.lightState = response;
				// And we flag that we should now be editing.
				LUMAStateService.isEditing = true;
			}
			// If the state query was unsuccessful...
			else
			{
				// We store the error message,
				LUMAStateService.errorMessage =
					'Error retrieving light state: '+response['message'];
				// And set the error flag.
				LUMAStateService.isError = true;
			}
		});		
	}
	
	// Submits a lighting pattern to the server.
	function performStateSubmit(uuid)
	{
		// Stop editing while we are submitting.
		LUMAStateService.isEditing = false;
		LUMAStateService.isError = false;
		LUMAStateService.errorMessage = '';
		
		// Format the light state into an object accepted by the API.
		var state = LUMAStateService.lightState;
		var request = {'uuid':uuid,'lights':[state]};
		console.log('REQUEST:');
		console.log(request);
		
		// Send our stuff!
		$http.post('resources/lights/state/'+JSON.stringify(request)).
		success(function(response)
		{
			console.log('RESPONSE:');
			console.log(response);
		});
		
	}
	
    return {
		// The function to submit a light query to the server.
		submitLightQuery: function(uuid, query){performLightQuery(uuid, query);},
		// The function to submit a light state query to the server.
		requestLightState: function(uuid, light){performStateQuery(uuid, light);},
		// The function to submit an updated light state to the server.
		submitLightState: function(uuid){performStateSubmit(uuid);}
    };
}]);