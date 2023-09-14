$(document).ready(function () {
        $('#query').focus();

        $('#glossaryDataTable').DataTable({
            "searching":false,
             "language": {
                url: 'https://cdn.datatables.net/plug-ins/1.12.1/i18n/es-ES.json'
                }
        });
        $('#categoryDataTable').DataTable({
            "initComplete":function () {
                $('#categoryDataTable_filter label input').focus();
            },
            "language": {
                url: 'https://cdn.datatables.net/plug-ins/1.12.1/i18n/es-ES.json'
            }
        });
        $('#problemCoppertable').DataTable( {
            "info": false,
             "language": {
                url: 'https://cdn.datatables.net/plug-ins/1.12.1/i18n/es-ES.json'
            }
	    });
    });