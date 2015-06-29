// LUMA Copyright (c) Gerard Geer 2014-2015 

// Just a simple bank of test lights.
var testLights = [ 	{id:"55e0ed38-2e14-45c2-aac9-c81740b16be1", name:"Gerard's Desk", client:"Gerard and Josh's Room"},
					{id:"51d784a7-8f30-4e02-9186-54440372e6a4", name:"Gerard's Bed", client:"Gerard and Josh's Room"},
					{id:"c89f6784-9611-4df4-8eee-dbf9cacf2f8e", name:"Josh's Bed", client:"Gerard and Josh's Room"},
					{id:"1eb9c4d2-7277-4469-a578-c36d7f09badb", name:'Research Room Shelves', client:'Research Room'},
					{id:"fbbe28a5-b1a1-4fc3-b133-bb6f8227f18e", name:'Research Room Countertop', client:'Research Room'},
					{id:"539eb5df-7ac0-4eff-929e-37a65c3cc1a9", name:'Research Room Left Window', client:'Research Room'},
					{id:"6c1a03e1-5c40-406c-99ca-181c1a73de7f", name:'Research Room Right Window', client:'Research Room'},
					{id:"fc2fb7a8-cabb-4859-a994-d684c34442bd", name:'Research Room Ceiling', client:'Research Room'},
					{id:"561519e7-f6a8-462b-a749-c7de69ade7d1", name:"Couch", client:"Max's Room"},
					{id:"3f827e77-444a-40be-8526-b3055f14848a", name:"Desk", client:"Max's Room"},
					{id:"d23c737a-269b-4ce9-9c05-cd9011ef20f9", name:"Bed", client:"Max's Room"},
					{id:"d2a7107e-9dbe-4e18-a3eb-364202a640d6", name:"Ceiling", client:"Max's Room"}];
					
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
		$http.get('resources/lights/'+'{"uuid":"3", "query":"'+query+'"}')
		.success(function(response)
		{
			console.log(response);
		});
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