// Print metadata in the slider by looping through the 
// links in the clean metadata file

function printMetadata(node_object){

	if(node_object.group == 2){
	
		document.getElementById("slider").innerHTML = 
		"<a href='https://osf.io/" + node_object.id + "' target='_blank'>" +
		node_object.label
		
		document.getElementById("slider").innerHTML += "<p><b>Contributors: </b></p>" 
    
		for (var i = 0; i < node_object.collab_name.length; i++) {
        
    		document.getElementById("slider").innerHTML += 
    		"<a href='https://osf.io/" + node_object.collab_id[i] + "' target='_blank'>" +
    		node_object.collab_name[i] + "</a><br>"
    
		} 

	} else {
	
		document.getElementById("slider").innerHTML = 
		"<a href='https://osf.io/" + node_object.id + "' target='_blank'>" +
		node_object.label + "</a> <p><b>Public Projects: </b></p><br>"
    
		for (var i = 0; i < node_object.project_name.length; i++) {
        
    		document.getElementById("slider").innerHTML += 
    		"<a href='https://osf.io/" + node_object.project_id[i] + "' target='_blank'>" +
    		node_object.project_name[i] + "</a><br><br>"
        
		}
        
		document.getElementById("slider").innerHTML += "<p><b>Collaborators: </b></p>" 
    
		for (var i = 0; i < node_object.collab_name.length; i++) {
        
    		document.getElementById("slider").innerHTML += 
    		"<a href='https://osf.io/" + node_object.collab_id[i] + "' target='_blank'>" +
    		node_object.collab_name[i] + "</a><br>"
    
		} 

	}

	console.log(node_object)

}

