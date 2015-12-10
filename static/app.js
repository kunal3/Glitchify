var glitchify = angular.module("glitchify", ["firebase"]);

function ImageController($scope, $firebase) {
	$scope.images = [{'path': 'images/apple.png'},
										{'path': 'images/girlphone.png'},
										{'path': 'images/ipad.png'}];
}

function VoteController($scope, $firebase, Firebase) {
	$scope.init = function(imgKey) {
    // bind Firebase data to scope variable 'data'
    var FBURL = "https://glitchify.firebaseio.com/images/";
    $scope.data = $firebase(new Firebase(FBURL + imgKey));

    // monitor data for updates and check weather setting
    $scope.data.$on('loaded', checkVotes);
    $scope.data.$on('change', checkVotes);

		$scope.updateCount = function(direction) {
			//Increment counter in Firebase using a transaction
			var directionRef = new Firebase(FBURL + imgKey + direction);
			directionRef.transaction(function(current_val) {
        // initialize the data if this imgKey hasn't been saved before
        if( !current_val ) { current_val = { upvote: 0, downvote: 0, direction: 0 }; }

        current_val.direction++;
        current_val[direction]++;
        return current_val;
			});
    };
	};

	//Check values to display sun or fog image
	function checkVotes() {
   	$scope.count = $scope.data.upvote - $scope.data.downvote;
		// if ($scope.data.sunny >= $scope.data.foggy) {
		// 	$scope.weather = "sunny";
		// } else {
		// 	$scope.weather = "foggy";
		// }
	}
}