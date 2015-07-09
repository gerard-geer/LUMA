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
		else if (nl.exists) nl.r_c=0;
		if (!nl.exists && isNaN( parseInt(nl.g_c) ) )
		{
			return 'Green pin number is not an integer.';
		}
		else if (nl.exists) nl.g_c=0;
		if (!nl.exists && isNaN( parseInt(nl.b_c) ) )
		{
			return 'Blue pin number is not an integer.';
		}
		else if (nl.exists) nl.b_c=0;
		
		return '';
	}
	
	function performLightAdd()
	{
		
		// Sanitize the light.
		test = sanitizeNewLight(AdminStateService.newLight);
		
		// If the light doesn't pass sanitation, we have to throw up the
		// ol' error box.
		if (test != '')
		{
			AdminStateService.errorMessage = test;
			AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.ERROR;
			return;
		}
		
		// Just a less verbose copy of the new light that we can manipulate.
		nl = {
			name: AdminStateService.newLight.name,
			client: AdminStateService.newLight.client,
			address: AdminStateService.newLight.address,
			permitted: AdminStateService.newLight.permitted,
			id: AdminStateService.newLight.id,
			exists: AdminStateService.newLight.exists,
			r_c: parseInt(AdminStateService.newLight.r_c),
			g_c: parseInt(AdminStateService.newLight.g_c),
			b_c: parseInt(AdminStateService.newLight.b_c)
		}
		
		// Split up the permitted string into a list, and trim the entries.
		nl.permitted = nl.permitted.split(',');
		for(var i = 0; i < nl.permitted.length; ++i)
		{
			// YOU SHALT NOT HAVE SPACES.
			nl.permitted[i] = nl.permitted[i].replace(/ /g,'');
		}
		
		// Finally we can send the request to the server.
		$http.post('resources/lights/', nl).
		success(function(response)
		{
			// Let's just go ahead and log the raw response.
			console.log("Light Add response:");
			console.log(response);
			
			// Now if the light was successful we close the add-light dialog.
			if(response.success)
			{
				AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.NO_DIALOG;
				AdminStateService.showDialog = true;
			}
			// And if it wasn't, we bring up the error dialog.
			else
			{
				AdminStateService.errorMessage = response.message;
				AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.ERROR;
				AdminStateService.showDialog = true;
			}
		}).
		error(function(response)
		{
			// Log the response anyhow.
			console.log("Light Add response:");
			console.log(response);
			// Bring up the error message.
			AdminStateService.errorMessage = response;
			AdminStateService.dialogToShow = AdminStateService.DIALOG_ENUM.ERROR;
			AdminStateService.showDialog = true;
		});
	}
	
    return {
		addNewLight: function(){performLightAdd();}
    };
}]);