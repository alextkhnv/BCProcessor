window.onload = function () {
    $('#parse').click(function() {
        console.log( "Handler for .click() called." );
        $.ajax({
            url: "../parse",
            success: function(res) {
                console.log(res);
                $('#parseContent').append('<pre>Status: ' + res.status + '\njobid: ' + res.jobid + '\nnode_name: ' + res.node_name + '</pre>');
            }
        })
    });
    $('#sync').click(function() {
        console.log( "Handler for .click() called." );
        $.ajax({
            url: "../sync",
            success: function(res) {
                console.log(res);
                //$('#parseContent').append('<pre>Status: ' + res.status + '\njobid: ' + res.jobid + '\nnode_name: ' + res.node_name + '</pre>');
            }
        })
    });
    $('#setDifference').click(function() {
        console.log( "Handler for .click() called." );
        $.ajax({
            url: "../set_difference",
            success: function(res) {
                console.log(res);
                //$('#parseContent').append('<pre>Status: ' + res.status + '\njobid: ' + res.jobid + '\nnode_name: ' + res.node_name + '</pre>');
            }
        })
    });
};