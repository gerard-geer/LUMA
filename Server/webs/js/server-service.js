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
		var lowercase = query.toLowerCase();
		
		// Create a stringified JSON object as our request.
		var request = JSON.stringify({'uuid':uuid,'query':query})
		
		// Send the request!
		$http.get('resources/lights/'+request)
		.success(function(response)
		{
			console.log("State query response:")
			console.log(response);
			// Get the lights for ease of use.
			var lights = response['lights'];
			
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
		var request = JSON.stringify({'uuid':uuid,'id':light['id']})
		
		// Send the request!
		$http.get('resources/lights/state/'+request)
		.success(function(response)
		{
			console.log("State query response:")
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
		// In the case of any error we want to prepend it
		// with 'Server error: '.
		LUMAStateService.errorMessage = 'Server error: ';
		
		// Format the light state into an object accepted by the API.
		var state = {
			'r_t': 	  LUMAStateService.lightState['r_t'],
			'r_v': 	  LUMAStateService.lightState['r_v'],
			'g_t': 	  LUMAStateService.lightState['g_t'],
			'g_v': 	  LUMAStateService.lightState['g_v'],
			'b_t': 	  LUMAStateService.lightState['b_t'],
			'b_v': 	  LUMAStateService.lightState['b_v'],
			'name':	  LUMAStateService.lightState['name'],
			'id': 	  LUMAStateService.lightState['id'],
			'client': LUMAStateService.lightState['client']
		}
		var request = {'uuid':uuid,'lights':[state]};
		
		// Send our stuff!
		$http.post('resources/lights/state/'+JSON.stringify(request)).
		success(function(response)
		{
			console.log("State update response:")
			console.log(response);
			// If the request failed at the request level, we need to
			// display an error.
			if(!response['success'])
			{
				LUMAStateService.errorMessage += 
					response['message'];
				LUMAStateService.isError = true;
				// Since there aren't any lights to parse through we just
				// return here.
				return;
			}
			
			// If the response failed for a light, well we have problems too.
			var lights = response['lights'];
			for(var i = 0; i < lights.length; ++i)
			{
				if(!lights[i]['success'])
				{
					LUMAStateService.errorMessage += 
						"'"+lights[i]['name']+"': "+lights[i]['message']+'\n';
					LUMAStateService.isError = true;
				}
			}
			
			// Otherwise we update our local model of the light state with
			// what was returned and bring back up the edit pane.
			LUMAStateService.lightState = lights[0];
			LUMAStateService.isEditing = !LUMAStateService.isError;
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