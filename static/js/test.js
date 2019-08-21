//exporte les données sélectionnées
 $(document).ready( function () {<font></font>
    $('#myTable').DataTable();<font></font>
} );<font></font>


// This file is required by the index.html file and will<font></font>
// be executed in the renderer process for that window.<font></font>
// All of the Node.js APIs are available in this process.<font></font>
window.$ = window.jquery = require('./node_modules/jquery');<font></font>
window.dt = require('./node_modules/datatables.net')();<font></font>
window.$('#table_id').DataTable();<font></font>