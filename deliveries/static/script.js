(function(){
	const form = document.querySelector('#frmDeliveriesLogin')
	form.addEventListener('submit', async e=>{
		e.preventDefault()

		const formdata = new FormData(form)
		
		const connection = await fetch( 'http://127.0.0.1:8000/api/v1/rest-auth/login/',{
			method: "POST",
			body: formdata
		})

		const response = await connection.json()

		if(response){
			localStorage.token = response.key
			window.location.href = 'profile'
		}
	})
}())