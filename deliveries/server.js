const path 		= require('path')
const express 	= require('express')
const app 		= express()

app.use(express.static('static'))

// ##################################################
app.get('/', (req,res)=>{
	res.sendFile( path.join( __dirname, "app", "index.html" ) )
})
// ##################################################
app.get('/profile/deliveries/:id', (req,res)=>{
	res.sendFile( path.join( __dirname, "app", "delivery-detail.html" ) )
})
// ##################################################
app.get('/profile', (req,res)=>{
	res.sendFile( path.join( __dirname, "app", "profile.html" ) )
})
// ##################################################


// function getDeliveryId() {

// }
app.listen(3000, err=>{
	if(err){
		console.log(`Error: ${err}`)
		return
	}
	console.log(`Listening to port 3000`)
})
process.on('uncaughtException', err=>{
	if(err){
		console.log(`Critical Error: ${err}`)
		return
	}
})