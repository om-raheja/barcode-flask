const bcrypt = dcodeIO.bcrypt;

var user = document.getElementById("user");
var password = document.getElementById("password");
function createUser() {
	const formData = new URLSearchParams();
	formData.append('user', user.value);

	var salt = bcrypt.genSaltSync(10);
	var hashed = bcrypt.hashSync(password.value, salt);

	formData.append("password", hashed);
	formData.append("salt", salt);

	fetch('/users', {
		method: 'POST',
		body: formData,
	})
	.then(response => response.json())
	.then(data => console.log(data));
}

function login() {
	const formData = new URLSearchParams();
	formData.append('user', user.value);


	// get the salt
	fetch('/login', {
		method: 'POST',
		body: formData,
	})
	.then(response => response.text())
	.then(salt => {
		formData.append('password', bcrypt.hashSync(password.value, salt));

		fetch('/login', {
			method: 'POST',
			body: formData,
		})
		.then(response => { 
			if (response.status != 204) {
				alert("Login failed.");
			} else {
				location.href = '/';
			}
		}); 
		
	});
} 
