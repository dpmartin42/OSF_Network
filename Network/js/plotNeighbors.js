// When a node is clicked, we check for each node
// if it is a neighbor of the clicked one. If not,
// we set its color as grey, and else, it takes its
// original color.
// We do the same for the edges, and we only keep
// edges that have both extremities colored.

s.bind('clickNode', function(e) {

    var nodeId = e.data.node.id,
        toKeep = s.graph.neighbors(nodeId);
    toKeep[nodeId] = e.data.node;

    s.graph.nodes().forEach(function(n) {
        if (toKeep[n.id])
            n.color = n.originalColor;
        else
            n.color = '#eee';
    });

    s.graph.edges().forEach(function(e) {
        if (toKeep[e.source] && toKeep[e.target]){
        	e.hidden = false;
        	e.color = e.originalColor;
        }	
        else
            e.hidden = true;
    });

    // Since the data has been modified, we need to
    // call the refresh method to make the colors
    // update effective.
    s.refresh();
    
    // Display metadata if node is clicked
    
    printMetadata(e.data.node);
    
    if($(".slider").is(":hidden")){
        $(".slider").toggle("slide", {direction: 'right'}, 1000);
    }
        
 });

// When the stage is clicked, we just color each
// node and edge with its original color.

s.bind('clickStage', function(e) {
	s.graph.nodes().forEach(function(n) {
    	n.color = n.originalColor;
    });

    s.graph.edges().forEach(function(e) {
        e.color = e.originalColor;
        e.hidden = false;
    });

    // Same as in the previous event:
    s.refresh();
    
    // If the slider is open, clicking on the sigma canvas will close it
    
    if($(".slider").is(":visible")){
        $(".slider").toggle("slide", {direction: 'right'}, 1000);
    }  
    
});

