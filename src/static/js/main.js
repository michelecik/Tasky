async function controller(action, parms) {
	var ret_val = {content: null, code: 0};
	
	await $.ajax({
		url: action,
		method: "POST",
		data: JSON.stringify(parms),
		dataType: 'json',
		success: function(result){
			ret_val = result;
		},
		error: function(){
			ret_val.code = 500;
		}
	});
	
	return ret_val;	
}
/* --- Memoria del login fatto secondo gli standard RESTFull ---
var credential = null;
function getCredential() {
	var credential = localStorage.getItem("credential");
	
	if ((credential !== undefined) && (credential != null)) {
		return JSON.parse(credential);
	} else {
		return null;
	}
}
*/