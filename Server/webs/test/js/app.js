
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
app.controller('QueryController', function(){
	// The query that will be sent to the server.
	this.query = null;
	this.response = null;
	this.submitted = false;
	
	// The submisison callback for the query form.
	this.onSubmit = function(){
		console.log(this.query);
		this.submitted = true;
		// The response from the server to this query.
		this.response = testLights;
	};
});
				
/*
	The Result Controller. Handles the functionality of each
	result.
*/
app.controller('ResultController', function(){
	this.onSelect = function(light){
		// Remove the search results so we can put something else in their
		// place, such as an edit pane.
		results = document.getElementById("search_results");
		results.parentNode.removeChild(results);
		this.selectedResult = light;
		console.log("selected light: \n"+light.name+"\n"+light.client);
	};
});