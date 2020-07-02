const path 		= require('path')
const cors 		= require('cors')

const express 	= require('express')
const app 		= express()

app.use(cors())
// app.use(express.static('static'))

app.get('/:img', (req,res)=>{
	const image = req.params.img
	return res.sendFile(path.join( __dirname, "static", image ))
})

app.listen(80, (err)=>{
	if(err){
		console.log(`Error: cannot listen to port 80.`)
		return
	}
	console.log(`Listening to port 80.`)
})
process.on("uncaughtException", (err)=>{
	if(err){
		console.log(`Critical Error!`)
		console.log(err)
		return
	}
})