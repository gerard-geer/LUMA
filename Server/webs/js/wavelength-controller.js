// LUMA Copyright (c) Gerard Geer 2014-2015 

angular.module('LUMAClient').controller('WavelengthController', 
['$scope','LUMAStateService', 
function($scope, LUMAStateService){
	
	// Bind the state service so we can access it in the DOM.
	$scope.state = LUMAStateService;
	
	// The canvas element.
	$scope.wCanvas = document.getElementById('wavelength_canvas');
	
	// The drawing context we pull from the canvas.
	$scope.wContext = $scope.wCanvas.getContext('2d');
	
	// Set up the drawing context.
	$scope.wContext.lineWidth = 2;
	
	// The default values for wavelengths of the three channels.
	$scope.rLambda = 1.0;
	$scope.gLambda = 1.0;
	$scope.bLambda = 1.0;

	
	// Returns the greatest common factor of two numbers.
	function gcf(a, b) { 
		return ( b == 0 ) ? (a):( gcf(b, a % b) ); 
	}
	// Returns the least common multiple of two numbers.
	function lcm(a, b) { 
		return ( a / gcf(a,b) ) * b; 
	}
	
	// Does the same thing for a set of numbers.
	function lcm_nums(ar) {
		if (ar.length > 1) {
			ar.push( lcm( ar.shift() , ar.shift() ) );
			return lcm_nums( ar );
		} else {
			return ar[0];
		}
	}
	
	// Draws a wavelength comparison line.
	function drawCompareLine(unit, wavelength, height, color)
	{
		$scope.wContext.beginPath();
		$scope.wContext.strokeStyle = color;
		$scope.wContext.rect(unit*wavelength-2, height-1, 2, 2);
		$scope.wContext.moveTo(0, height);
		$scope.wContext.lineTo(unit*wavelength, height);
		$scope.wContext.stroke();
	}
	
	function drawCycleLine(gap, width, height, color)
	{
		$scope.wContext.beginPath();
		$scope.wContext.strokeStyle = color;
		$scope.wContext.moveTo(0, height);
		$scope.wContext.lineTo(width, height);
		for(var i = 0; i < width; i+=width/gap)
		{
			$scope.wContext.rect(i-1, height-1, 2, 2);
		}
		$scope.wContext.stroke();
	}
	
	// Updates the wavelength preview canvas.
	this.updatePreview = function(){

		$scope.wContext.clearRect(0, 0, $scope.wCanvas.width, 25);
		
		var longest = 0;
		longest = (longest > $scope.rLambda) ? longest : $scope.rLambda;
		longest = (longest > $scope.gLambda) ? longest : $scope.gLambda;
		longest = (longest > $scope.bLambda) ? longest : $scope.bLambda;
		
		var unit = $scope.wCanvas.width / longest;
		// Simple length comparison lines.
		drawCompareLine(unit, $scope.rLambda, 5,  '#FF0000');
		drawCompareLine(unit, $scope.gLambda, 10,  '#00FF00');
		drawCompareLine(unit, $scope.bLambda, 15, '#0000FF');
		
		if($scope.rLambda > 0 && $scope.gLambda > 0 && $scope.bLambda > 0)
		{
			$scope.wContext.clearRect(0, 25, $scope.wCanvas.width, 25);
			
			var mult = lcm_nums([	parseInt(Math.floor($scope.rLambda)),
									parseInt(Math.floor($scope.gLambda)),
									parseInt(Math.floor($scope.bLambda))]);
			// At this point drawing extra would be futile.
			mult = (mult > 500*longest) ? 500*longest : mult;
			drawCycleLine(mult/parseInt(Math.floor($scope.rLambda)), $scope.wCanvas.width, 35, '#FF0000');
			drawCycleLine(mult/parseInt(Math.floor($scope.gLambda)), $scope.wCanvas.width, 40, '#00FF00');
			drawCycleLine(mult/parseInt(Math.floor($scope.bLambda)), $scope.wCanvas.width, 45, '#0000FF');
		}
	}
	this.updatePreview();
	
	// Gets the wavelength of a channel by integrating over its
	// time steps.
	function getWavelength(timings)
	{
		// In the waveform paradigm it is convenient that
		// all time steps are equal.
		return timings[0]*timings.length;
	}
	
	// Sets the wavelength of a channel.
	function setWavelength(timings, wavelength)
	{
		var timing = wavelength/timings.length; 
		for(var i = 0; i < timings.length; ++i)timings[i] = timing;
	}
	
	this.onSubmit = function()
	{
		setWavelength(LUMAStateService.lightState.r_t, $scope.rLambda);
		setWavelength(LUMAStateService.lightState.g_t, $scope.gLambda);
		setWavelength(LUMAStateService.lightState.b_t, $scope.bLambda);
		this.updatePreview();
	}
		
	// Whenever the light state is populated, then this watch function
	// will be triggered and will update the model with proper values.
	$scope.$watch(function() {
		return LUMAStateService.lightState;
	},
	function() {
		if(LUMAStateService.lightState != null)
		{
			$scope.rLambda = getWavelength(LUMAStateService.lightState.r_t);
			$scope.gLambda = getWavelength(LUMAStateService.lightState.g_t);
			$scope.bLambda = getWavelength(LUMAStateService.lightState.b_t);
			//this.updatePreview();
		}
	});
}]);