
// Just a simple bank of test lights.
var testLights = [ 	{name:"Gerard's Desk", client:"Gerard and Josh's Room"},
					{name:"Gerard's Bed", client:"Gerard and Josh's Room"},
					{name:"Josh's Bed", client:"Gerard and Josh's Room"},
					{name:'Research Room Shelves', client:'Research Room'},
					{name:'Research Room Countertop', client:'Research Room'},
					{name:'Research Room Left Window', client:'Research Room'},
					{name:'Research Room Right Window', client:'Research Room'},
					{name:'Research Room Ceiling', client:'Research Room'},
					{name:"Couch", client:"Max's Room"},
					{name:"Desk", client:"Max's Room"},
					{name:"Bed", client:"Max's Room"},
					{name:"Ceiling", client:"Max's Room"}];
					
var testState = {	success: true,
					message: "simple message from client of Couch",
					name: "Couch",
					client: "Max's Room",
					r_t: [0,1],
					r_v: [0,1],
					r_c: 0,
					g_t: [0,1],
					g_v: [0,1],
					g_c: 0,
					b_t: [0,1],
					b_v: [0,1],
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
		// Convert the query to lower-case for better comparison.
		lowercase = query.toLowerCase();
		// Go through each of the dummy lights, and if it matches
		// add it to the response.
		for(var i = 0; i < testLights.length; ++i)
		{
			if(	testLights[i].name.toLowerCase().indexOf(lowercase) >= 0 ||
			testLights[i].client.toLowerCase().indexOf(lowercase) >= 0 )
				LUMAStateService.queryResults.push(testLights[i]);
		}
		console.log('RESPONSE LENGTH BRAH: '+LUMAStateService.queryResults.length);
	}
	
	// "Requests from the server the state of the light."
	function performStateQuery(uuid, light)
	{
		LUMAStateService.lightState = testState;
	}

    return {
		// The function to submit a light query to the server.
		submitLightQuery: function(uuid, query){performLightQuery(uuid, query);},
		// The function to submit a light state query to the server.
		requestLightState: function(uuid, light){performStateQuery(uuid, light);}
    };
}]);