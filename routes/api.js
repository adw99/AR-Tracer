var express = require('express');
var router = express.Router();

// Models
var Bear =require('../models/bear');

/* debug middleware */
router.use( function( req, res, next ) {

	console.log("API request happened");
	next();
});

/* GET users listing. */
router.get('/', function(req, res) {
  res.json({ message: 'API version 0.0.0.1 working'} );
});


router.post( '/bears', function(req,res) {

	var bear = new Bear();
	bear.name = req.body.name;

	console.log("createing bear with name:" + req.body.name );
	console.log("request body:", req.body);

	bear.save( function(err) {
		if( err ) 
			res.send(err);
		res.json( {message: 'Bear created'});
	})
});


router.get('/bears', function(req,res) {
	Bear.find( function(err,bears) {
		if( err )
			res.send(err);
		res.json(bears);
	})
});


router.get('/bears/:bear_id',function(req,res) {
	Bear.findById( req.params.bear_id, function(err,bear) {
		if( err )
			res.send(err);
		res.json(bear);
	})
});

router.put('/bears/:bear_id', function(req,res) {
	Bear.findById( req.params.bear_id, function(err,bear) {
		if( err )
			res.send(err);
		bear.name = req.body.name;

		console.log('new name:' + req.body.name );
		console.log('request:',req.body);
		bear.save(function(err) {
			if( err )
				res.send(err);

			res.json( {message:'Bear updated!'});
		});
	})

});

router.delete('/bears/:bear_id',function(req,res) {
	Bear.remove({ _id: req.params.bear_id }, function(err,bear) {
		if(err)
			res.send(err);
		res.json({message:'Successfully deleted'});
	});
});

module.exports = router;

