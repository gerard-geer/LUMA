/*
	The Waveform Controller. Handles the functionality of the waveform
	paradigm editing widget.
*/
angular.module('LUMAClient').controller('WaveformController', 
['$scope','LUMAServerService','LUMAStateService',
function($scope,LUMAServerService,LUMAStateService){
	
	// Bind the controller's scope to the state service.
	$scope.state = LUMAStateService;
	
	// The currently selected channel.
	$scope.channel = 'red';
	
	// Whether or not the wavelength dialog is visible.
	$scope.showPeriodDialog = false;
	
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
	$scope.state.r_v = Array();
	$scope.state.g_v = Array();
	$scope.state.b_v = Array();
	
	// Redraws a line.
	function update(ctx, index, val, numVals)
	{
		// Go ahead and scale the index so we can
		// use it as the drawing x-coordinate.
		index *= ctx.canvas.width/numVals;
		// Clear the region of the line.
		ctx.clearRect(index-3, 0, 6, ctx.canvas.height);
		
		// Draw the new line.
		ctx.beginPath();
		ctx.lineWidth = 2;
		ctx.moveTo(index, ctx.canvas.height);
		ctx.lineTo(index, ctx.canvas.height-ctx.canvas.height*val);
		ctx.rect(index-1.25, ctx.canvas.height-2, 2.5, 1);
		ctx.rect(index-1.25, ctx.canvas.height-ctx.canvas.height*val, 2.5, 1);
		ctx.stroke();
	}
	
	// Redraws all lines for a canvas.
	function updateAll(ctx, vals)
	{
		for(var i = 0; i < vals.length; ++i)
		{
			update(ctx, i, vals[i], vals.length);
		}
	}
	
	// The sine-wave preset function.
	this.sine = function(ctx, vals)
	{
		var length = vals.length;
		var period = 3.1459/length;
		vals.length = 0;
		for(var i = 0; i < length; ++i)
		{
			vals.push( Math.pow( Math.sin(i*period), 2 ) );
		}
		updateAll(ctx, vals);
	}
	// The sawtooth preset function.
	this.saw = function(ctx, vals)
	{
		var length = vals.length;
		vals.length = 0;
		for(var i = 0; i < length; ++i)
		{
			vals.push( i/length );
		}
		updateAll(ctx, vals);
	}
	// The reverse sawtooth preset function.
	this.revsaw = function(ctx, vals)
	{
		var length = vals.length;
		vals.length = 0;
		for(var i = 0; i < length; ++i)
		{
			vals.push( 1.0-(i/length) );
		}
		updateAll(ctx, vals);
	}
	// The square-wave preset function.
	this.square = function(ctx, vals)
	{
		var length = vals.length;
		vals.length = 0;
		for(var i = 0; i < length; ++i)
		{
			vals.push( Math.floor( 2.0*(i/128) ) );
		}
		updateAll(ctx, vals);
	}
	// The triangle squarewave function.
	this.triangle = function(ctx, vals)
	{
		var length = vals.length;
		vals.length = 0;
		for(var i = 0; i < parseInt(Math.floor(length/2)); ++i)
		{
			vals.push( i/parseInt(Math.floor(length/2)) );
		}
		for(var i = parseInt(Math.floor(length/2)); i < length; ++i)
		{
			vals.push( 1.0-((i-parseInt(Math.floor(length/2)))/parseInt(Math.floor(length/2))) );
		}
		updateAll(ctx, vals);
	}
	// Empties the waveform, resetting every sample to zero.
	this.clear = function(ctx, vals)
	{
		for(var i = 0; i < vals.length; ++i)
		{
			vals[i] = 0;
		}
		updateAll(ctx, vals);
	}
	
	// Initialize them all with dummy values.
	for(var i = 0; i < 128; ++i)
	{
		$scope.state.r_v.push( Math.sin(i*.1)*Math.sin(i*.1) );
		$scope.state.g_v.push( Math.sin(i*.05)*Math.sin(i*.05) );
		$scope.state.b_v.push( Math.sin(i*.01)*Math.sin(i*.01) );
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
	updateAll($scope.rCtx, $scope.state.r_v);
	updateAll($scope.gCtx, $scope.state.g_v);
	updateAll($scope.bCtx, $scope.state.b_v);
	
	$scope.$watch(function() {
		return LUMAStateService.lightState;
	},
	function() {
		if(LUMAStateService.lightState != null)
		{
			
			$scope.state = LUMAStateService.lightState;
			$scope.rCtx.clearRect(0, 0, $scope.rCtx.canvas.width, $scope.rCtx.canvas.height);
			$scope.gCtx.clearRect(0, 0, $scope.gCtx.canvas.width, $scope.gCtx.canvas.height);
			$scope.bCtx.clearRect(0, 0, $scope.bCtx.canvas.width, $scope.bCtx.canvas.height);
			updateAll($scope.rCtx, $scope.state.r_v);
			updateAll($scope.gCtx, $scope.state.g_v);
			updateAll($scope.bCtx, $scope.state.b_v);
		}
	});
	
	// A function that takes the mouse position and finds the closest
	// value line to it, and updates it.
	function updateVal(canvas, ctx, evt, vals)
	{
		console.log("TRYIN TO UPDAHT");
		if(mdown)
		{
			// Get the mouse position.
			var pos = getMousePos(canvas, evt);
			// Get the index of the value to update.
			var index = parseInt(Math.round((pos.x/canvas.width)*vals.length));
			var val = 1 - (pos.y/canvas.height);
			// Update the value.
			vals[index] = val;
			
			update(ctx, index, val, vals.length);
		}
	}
	
	// A function that rotates a waveform's values left by 1/128 its period.
	this.rotateLeft = function(ctx, vals)
	{
		var first = vals[0];
		for(var i = 0; i < vals.length-1; ++i)
		{
			vals[i] = vals[i+1];
		}
		vals[vals.length-1]=first;
		updateAll(ctx, vals);
	}
	// A sister function that rotates right.
	this.rotateRight = function(ctx, vals)
	{
		var last = vals[vals.length-1];
		for(var i = vals.length-1; i > 0; --i)
		{
			vals[i] = vals[i-1];
		}
		vals[0] = last;
		updateAll(ctx, vals);
	}
	
	// Add the mouse up/down listeners so we can know when we're taking a drag.
	// Oh, and we also want functionality on click, so we update on mouse-down.
	$scope.rCanvas.addEventListener('mousedown', function(evt){
		mdown=true;
		updateVal($scope.rCanvas, $scope.rCtx, evt, $scope.state.r_v);
	},false);
	$scope.gCanvas.addEventListener('mousedown', function(){
		mdown=true;
		updateVal($scope.gCanvas, $scope.gCtx, evt, $scope.state.g_v);
	},false);
	$scope.bCanvas.addEventListener('mousedown', function(){
		mdown=true;
		updateVal($scope.bCanvas, $scope.bCtx, evt, $scope.state.b_v);
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
		updateVal($scope.rCanvas, $scope.rCtx, evt, $scope.state.r_v);
	},false);
	$scope.gCanvas.addEventListener('mousemove', function(evt){
		updateVal($scope.gCanvas, $scope.gCtx, evt, $scope.state.g_v);
	},false);
	$scope.bCanvas.addEventListener('mousemove', function(evt){
		updateVal($scope.bCanvas, $scope.bCtx, evt, $scope.state.b_v);
	},false);
	
	// A function that raises the wavelength dialog.
	$scope.raisePeriodDialog = function()
	{
		$scope.showPeriodDialog = true;
		document.getElementById('wavelength_cancel').focus();
	}
	
	// A sister function that lowers that dialog.
	$scope.supressPeriodDialog = function()
	{
		$scope.showPeriodDialog = false;
	}
	
	
}]);