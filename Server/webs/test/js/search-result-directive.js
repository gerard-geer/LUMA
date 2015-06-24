angular.module('LUMAClient', []).directive('lumaSearchResult', function() {
	return {
		restrict: 'A',
		replace: true,
		template:   
		"<div class='search_result'>"+
		"	<div class='result_content'>"+
		"		<div class='light_info'>"+
		"			<div class='light name'>"+
		"				<p class='label'>Name: </p>{{light.name}}"+
		"			</div>"+
		"			<div class='light client'>"+
		"				<p class='label'>Client: </p>{{light.client}}"+
		"			</div>"+
		"		</div>"+
		"	</div>"+
		"</div>"
	};
});