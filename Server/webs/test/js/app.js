(
	var app = angular.app("LUMA", []);
	
	var testLights = [ 	{name:'A', client:'A-C'},
						{name:'B', client:'A-C'},
						{name:'C', client:'B-C'} ];
			
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
		
		// The response from the server to this query.
		this.response = testLights;
	});
					
	/*
		The Result Controller. Gives each result interactivity.
	*/
	app.controller('ResultController', function(){
		this.onSelect = function(light){
			this.selectedResult = light;
		}		
	});
)();