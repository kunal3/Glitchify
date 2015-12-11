glitchify = angular.module("glitchify", ["firebase"]);

// console.log("glitchify: ", glitchify);

glitchify.controller("ImageController", ['$scope', '$firebase', 'Firebase', function ($scope, $firebase, Firebase) {
	// console.log("ImageController");
	var fb = new Firebase("https://glitchify.firebaseio.com/images");
	console.log("fb: ", fb);
	$scope.images = []
	fb.orderByKey().limitToFirst(7).once('value', function(dataSnapshot) {
	  if( dataSnapshot.val() ) {
	  	var snap = dataSnapshot.val();
	  	for(var key in snap) {
	  		// console.log("key: ", key);
	  		// console.log("snap[key]['filename']: ", snap[key]['filename']);
	  		$scope.images.push({
	  			'path': 'imgOut/'+snap[key]['filename'],
	  			'key': key
	  		});
	  		$scope.$digest()
	  	}
	  }
	  console.log("$scope.images: ", $scope.images);
	});

	$scope.init = function(imgKey) {
		// bind Firebase data to scope variable 'data'
		$scope.data = $firebase(new Firebase(fb + imgKey));

		// monitor data for updates and check weather setting
		$scope.data.$on('loaded', checkVotes);
		$scope.data.$on('change', checkVotes);

		$scope.updateCount = function(direction) {
			//Increment counter in Firebase using a transaction
			var directionRef = new Firebase(fb + '/' + imgKey + '/' + direction);
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
	}

	// fb.once('value', function(dataSnapshot) {
	//   if( dataSnapshot.val() ) {
	//   	var snap = dataSnapshot.val();
	//   	for(var key in snap) {
	//   		console.log("key: ", key);
	//   		console.log("snap[key]['filename']: ", snap[key]['filename']);
	//   		$scope.images.push({
	//   			'path': 'imgOut/'+snap[key]['filename'],
	//   			'key': key
	//   		});
	//   		$scope.$digest()
	//   	}
	//   }
	//   console.log("$scope.images: ", $scope.images);
	// });
}]);


	// $scope.init = function(imgKey) {
	// 	// bind Firebase data to scope variable 'data'
	// 	var FBURL = "https://glitchify.firebaseio.com/images/";
	// 	$scope.data = $firebase(new Firebase(FBURL + imgKey));

	// 	// monitor data for updates and check weather setting
	// 	$scope.data.$on('loaded', checkImages);
	// 	$scope.data.$on('change', checkImages);

	// 	// $scope.updateCount = function(direction) {
	// 	// 	//Increment counter in Firebase using a transaction
	// 	// 	var directionRef = new Firebase(FBURL + imgKey + direction);
	// 	// 	directionRef.transaction(function(current_val) {
	// 	// 		// initialize the data if this imgKey hasn't been saved before
	// 	// 		if( !current_val ) { current_val = { upvote: 0, downvote: 0, direction: 0 }; }

	// 	// 		current_val.direction++;
	// 	// 		current_val[direction]++;
	// 	// 		return current_val;
	// 	// 	});
	// 	// };
	// };

	// //Check values to display sun or fog image
	// function checkImages() {
	// 	$scope.images = [{'path': 'images/'+},
	// 										{'path': 'images/girlphone.png'},
	// 										{'path': 'images/ipad.png'}];
	// }
// }

function VoteController($scope, $firebase, Firebase) {
	
}