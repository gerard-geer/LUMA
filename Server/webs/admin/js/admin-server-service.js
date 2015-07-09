// LUMA Copyright (c) Gerard Geer 2014-2015 
					
/*
	The lUMA Server Service. This functions as a singleton that
	encapsulates interactions with the server, and stores the
	selected query result and the state of the requested light.
*/
angular.module('LUMAClientAdminPortal').factory('AdminServerService', 
['$http', 'AdminStateService', function($http, AdminStateService) {
	
	// Sanitizes the values passed in for the new light.
	function sanitizeNewLight(nl)
	{
		if (nl.name == null || nl.name == '')
		{
			return 'Name must be a non-empty string.';
		}
		if (nl.client == null || nl.client == '')
		{
			return 'Client must be a non-empty string.';
		}
		if (nl.address == null || nl.address == '')
		{
			return 'Address must be a non-empty string.';
		}
		if (nl.permitted == null || nl.permitted == '')
		{
			return 'Permitted must contain at least one UUID.';
		}
		if (nl.exists && (nl.id == null || nl.id == ''))
		{
			return 'ID must be a non-empty string.';
		}
		else if (!nl.exists) nl.id='';
		if (!nl.exists && isNaN( parseInt(nl.r_c) ) )
		{
			return 'Red pin number is not an integer.';
		}
		else if (!nl.exists) nl.r_c=0;
		if (!nl.exists && isNaN( parseInt(nl.g_c) ) )
		{
			return 'Green pin number is not an integer.';
		}
		else if (!nl.exists) nl.g_c=0;
		if (!nl.exists && isNaN( parseInt(nl.b_c) ) )
		{
			return 'Blue pin number is not an integer.';
		}
		else if (!nl.exists) nl.b_c=0;
		
		return '';
	}
	
	function performLightAdd()
	{
		nl = AdminStateService.newLight;
		test = sanitizeNewLight(nl)
		if (test != '')
		{
			AdminStateService.errorMessage = test;
			AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.ERROR;
			return;
		}
		
		$http.post('resources/lights/', nl).
		success(function(response)
		{
			console.log("Light Add response:");
			console.log(response);
		}).
		error(function(response)
		{
			console.log("Light Add response:");
			console.log(response);
			AdminStateService.errorMessage = response;
			AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.ERROR;
		});
	}
	
    return {
		addNewLight: function(){performLightAdd();}
    };
}]);