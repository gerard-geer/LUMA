
// Create our Angular module, which depends on ngAnimate.
var app = angular.module('LumaClient', ['ngAnimate']);

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
		
// The user's selection from the original query.
var selectedResult = null;

// The entirety of the light selected by the user,
// returned by the server for editing locally.
var selectedLight = null;
					
/*
	The QueryController. Handles functionality regarding
	the querying of the light server for valid light instances.
*/
app.controller('QueryController', ['$animate', function($animate){
	// The query that will be sent to the server.
	this.query = null;
	// Our fake response from the server.
	this.response = new Array();
	// Whether or not this query has been submitted.
	this.submitted = false;
	
	// The submisison callback for the query form.
	this.onSubmit = function(){
			
		this.submitted = true;
		this.response = Array();
		this.query = this.query.toLowerCase();
		for(var i = 0; i < testLights.length; ++i)
		{
			if(	testLights[i].name.toLowerCase().indexOf(this.query) >= 0 ||
			testLights[i].client.toLowerCase().indexOf(this.query) >= 0 )
				this.response.push(testLights[i]);
		}
	};
}]);
				
/*
	The Result Controller. Handles the functionality of each
	result.
*/
app.controller('ResultController', function(){
	this.onSelect = function(light, query){
		// Remove the search results so we can put something else in their
		// place, such as an edit pane.
		query.response = Array();
		this.selectedResult = light;
		console.log("selected light: \n"+light.name+"\n"+light.client);
	};
});