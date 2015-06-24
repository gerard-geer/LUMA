angular.module('LUMAClient', []).directive('lumaSearchResults', function() {
  return {
    restrict: 'E',
	replace: false,
	transclude: true,
    template:   
		"<div id='search_results' ng-transclude>"+
		"</div>"
	};
});