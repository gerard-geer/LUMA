// Create our Angular module.
var app = angular.module('LumaClient', ['rzModule']);

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

// The entirety of the light selected by the user,
// returned by the server for editing locally.
var lightToEdit = null;
					
/*
	The QueryController. Handles functionality regarding
	the querying of the light server for valid light instances.
*/
app.controller('QueryController', ['$animate', '$rootScope', function($animate, $rootScope){
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
				
/*
	The Result Controller. Handles the functionality of each
	result.
*/
app.controller('ResultController', ['$rootScope', function($rootScope){
	
	this.onSelect = function(light, query){
		// Remove the search results so we can put something else in their
		// place, such as an edit pane.
		query.response = Array();
		console.log("selected light: \n"+light.name+"\n"+light.client);
		lightToEdit = testState;
		$rootScope.isEditing = true;
	};
}]);

/*
	The Waveform Controller. Handles the functionality of the waveform
	paradigm editing widget.
*/
app.controller('WaveformController', function($scope){
	$scope.$broadcast('refreshSlider')
	// The currently selected channel.
	$scope.channel = 'red';
	
	// The periods of the channel waveforms.
	$scope.rPeriod = 0.5;
	$scope.gPeriod = 0.5;
	$scope.bPeriod = 0.5;
	
	// Whether or not the mouse is down, so that we can
	// distinguish between moving and dragging.
	var mdown = false;
	
	// The three canvases.
	$scope.rCanvas = document.getElementById('red_canvas');
	$scope.gCanvas = document.getElementById('green_canvas');
	$scope.bCanvas = document.getElementById('blue_canvas');
	
	// The various canvases' rendering contexts.
	$scope.rCtx = $scope.rCanvas.getContext('2d');	
	$scope.gCtx = $scope.gCanvas.getContext('2d');	
	$scope.bCtx = $scope.bCanvas.getContext('2d');
	
	$scope.rCtx.strokeStyle = '#FF0000';
	$scope.gCtx.strokeStyle = '#00FF00';
	$scope.bCtx.strokeStyle = '#0000FF';
	
	// The arrays of brightness values.
	$scope.rVals = Array();
	$scope.gVals = Array();
	$scope.bVals = Array();
	
	this.sine = function(ctx, vals, color)
	{
		vals.length = 0;
		for(var i = 0; i < 128; ++i)
		{
			//								2PI/128
			vals.push( Math.pow( Math.sin(i*.024544), 2 ) );
		}
		updateAll(ctx, vals, color);
	}
	this.saw = function(ctx, vals, color)
	{
		vals.length = 0;
		for(var i = 0; i < 128; ++i)
		{
			vals.push( i/128 );
		}
		updateAll(ctx, vals, color);
	}
	this.revsaw = function(ctx, vals, color)
	{
		vals.length = 0;
		for(var i = 0; i < 128; ++i)
		{
			vals.push( 1.0-(i/128) );
		}
		updateAll(ctx, vals, color);
	}
	this.square = function(ctx, vals, color)
	{
		vals.length = 0;
		for(var i = 0; i < 128; ++i)
		{
			vals.push( Math.floor( 2.0*(i/128) ) );
		}
		updateAll(ctx, vals, color);
	}
	this.triangle = function(ctx, vals, color)
	{
		vals.length = 0;
		for(var i = 0; i < 64; ++i)
		{
			vals.push( i/64 );
		}
		for(var i = 64; i < 128; ++i)
		{
			vals.push( 1.0-((i-64)/64) );
		}
		updateAll(ctx, vals, color);
	}
	// Initialize them all with dummy values.
	for(var i = 0; i < 128; ++i)
	{
		$scope.rVals.push( Math.sin(i*.1)*Math.sin(i*.1) );
		$scope.gVals.push( Math.sin(i*.05)*Math.sin(i*.05) );
		$scope.bVals.push( Math.sin(i*.01)*Math.sin(i*.01) );
	}
	
	// Redraws a line.
	function update(ctx, index, val, color)
	{
		index *= 8;
		
		// Clear the region of the line.
		ctx.clearRect(index-2, 0, 4, 576);
		
		// Draw the new line.
		ctx.beginPath();
		ctx.strokeStyle = color;
		ctx.lineWidth = 2;
		ctx.moveTo(index, 576);
		ctx.lineTo(index, 576-576*val);
		ctx.stroke();
	}
	
	// Redraws all lines for a canvas.
	function updateAll(ctx, vals, color)
	{
		for(var i = 0; i < 128; ++i)
		{
			update(ctx, i, vals[i], color);
		}
	}
	
	// A quick function that gets the mouse position on a canvas.
    function getMousePos(canvas, evt) {
		var rect = canvas.getBoundingClientRect();
		return {
			x: evt.clientX - rect.left,
			y: evt.clientY - rect.top
		};
    }
	
	// Draw all the initial values to the screen.
	updateAll($scope.rCtx, $scope.rVals, '#FF0000');
	updateAll($scope.gCtx, $scope.gVals, '#00FF00');
	updateAll($scope.bCtx, $scope.bVals, '#0000FF');
	
	// A function that takes the mouse position and finds the closest
	// value line to it, and updates it.
	function updateVal(canvas, ctx, evt, vals, color)
	{
		if(mdown)
		{
			// Get the mouse position.
			var pos = getMousePos(canvas, evt);
			// Get the index of the value to update.
			var index = parseInt((pos.x/canvas.width)*vals.length);
			var val = 1 - (pos.y/canvas.height);
			// Update the value.
			vals[index] = val;
			
			update(ctx, index, val, color);
		}
	}
	
	// Add the mouse up/down listeners so we can know when we're taking a drag.
	// Oh, and we also want functionality on click, so we update on mouse-down.
	$scope.rCanvas.addEventListener('mousedown', function(evt){
		mdown=true;
		updateVal($scope.rCanvas, $scope.rCtx, evt, $scope.rVals, '#FF0000');
	},false);
	$scope.gCanvas.addEventListener('mousedown', function(){
		mdown=true;
		updateVal($scope.gCanvas, $scope.gCtx, evt, $scope.gVals, '#00FF00');
	},false);
	$scope.bCanvas.addEventListener('mousedown', function(){
		mdown=true;
		updateVal($scope.bCanvas, $scope.bCtx, evt, $scope.bVals, '#0000FF');
	},false);
	$scope.rCanvas.addEventListener('mouseup', function(){mdown=false;},false);
	$scope.gCanvas.addEventListener('mouseup', function(){mdown=false;},false);
	$scope.bCanvas.addEventListener('mouseup', function(){mdown=false;},false);
	
	// When the mouse leaves the canvas, we want it to perk up a bit.
	$scope.rCanvas.addEventListener('mouseout', function(){mdown=false;},false);
	$scope.gCanvas.addEventListener('mouseout', function(){mdown=false;},false);
	$scope.bCanvas.addEventListener('mouseout', function(){mdown=false;},false);
	
	
	// Add the mouse move functions, which update the model if the mouse
	// is dragged.
	$scope.rCanvas.addEventListener('mousemove', function(evt){
		updateVal($scope.rCanvas, $scope.rCtx, evt, $scope.rVals, '#FF0000');
	},false);
	$scope.gCanvas.addEventListener('mousemove', function(evt){
		updateVal($scope.gCanvas, $scope.gCtx, evt, $scope.gVals, '#00FF00');
	},false);
	$scope.bCanvas.addEventListener('mousemove', function(evt){
		updateVal($scope.bCanvas, $scope.bCtx, evt, $scope.bVals, '#0000FF');
	},false);
});