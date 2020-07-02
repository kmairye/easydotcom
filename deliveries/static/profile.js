(async function(){

	// Initial connection to get all deliveries
	const connection = await fetch( 'http://127.0.0.1:8000/api/v1/',{
		method: "GET",
	})

	// Response json
	const response = await connection.json()
	
	// Handle result
	if(response){
		displayDeliveries(response)
	}
	
}())

function displayDeliveries(deliveries){
	
	// Get list
	const list = document.getElementById('deliveryList')
	
	// Get template
	const template = document.getElementById('deliveryTemplate').content
	
	// Loop thorugh deliveries
	deliveries.forEach(delivery=>{
		
		// Clone template
		const clone = template.cloneNode(true)
		
		// Set content
		clone.querySelector('.id').textContent 				= delivery.id
		clone.querySelector('.driver').textContent 			= delivery.driver
		clone.querySelector('.address').textContent 		= delivery.address
		clone.querySelector('.full-address').textContent 	= delivery.get_full_address
		clone.querySelector('.order').textContent 			= delivery.order
		clone.querySelector('.status').textContent 			= delivery.status
		clone.querySelector('.absolute-url').setAttribute('data-delivery-id', delivery.id)
		
		// Append new elms to list
		list.appendChild(clone)	
	})
	
	// Call detail view enabler function
	enableDetailedView()
}

function enableDetailedView(){

	// Get btns => to array
	const buttons = document.querySelectorAll('.absolute-url')
	const buttonsArr = Array.from(buttons)
	
	// For each loop
	buttonsArr.forEach(e=>{

		// Get id of obj
		const id = e.getAttribute('data-delivery-id')
		
		// Enable on-click event
		e.addEventListener('click', async e=>{
			
			// Create custom header
			const headers = new Headers()
			headers.append('Authorization', `Token ${localStorage.token}`)
			
			// Fetch
			const connection = await fetch(`http://127.0.0.1:8000/api/v1/${id}`, {
				method: "GET",
				headers: headers
			})

			// Respones.json
			const response = await connection.json()
			if(response){
				
				// Transfer data to form
				const form 		= document.querySelector('#frmUpdateDestroyDelivery')
				
				// Input values
				form.querySelector('#id').value = response.id
				form.querySelector('#driver').value = response.driver
				form.querySelector('#address').value = response.address
				form.querySelector('#order').value = response.order
				form.querySelector('#status').value = response.status
				
				submitUpdateDestroyDelivery()
			}		
		})
	})
}

function submitUpdateDestroyDelivery(){
	
	// The form
	const form 		= document.querySelector('#frmUpdateDestroyDelivery')
	form.addEventListener('submit', async(e)=>{

		// Create formdata()
		const formdata 	= new FormData()
		
		// Get values from form elms
		const username 			= form.querySelector('#username').value
		const email 			= form.querySelector('#email').value
		const password 			= form.querySelector('#password').value
		const id 				= form.querySelector('#id').value
		const driver 			= form.querySelector('#driver').value
		const address 			= form.querySelector('#address').value
		const order 			= form.querySelector('#order').value
		const status 			= form.querySelector('#status').value	
		
		// Append to request form data
		formdata.append('username', username)
		formdata.append('email', email)
		formdata.append('password', password)
		formdata.append('id', id)
		formdata.append('driver', driver)
		formdata.append('address', address)
		formdata.append('order', order)
		formdata.append('status', status)

		// Create custom header
		const headers = new Headers()

		// Append auth token
		headers.append('Authorization', `Token ${localStorage.token}`)

		// Fetch
		const connection = await fetch( `http://localhost:8000/api/v1/modify/${id}`, {
			method: "PATCH",
			headers: headers,
			body: formdata
		})
		
		// Response json
		const response = await connection.json()

		// Handle result
		if(response){
			console.log(repsonse)
		}
	})
}