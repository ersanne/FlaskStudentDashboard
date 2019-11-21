$(document).ready(function () {
    $('.select2-skills').select2({
        tags: true,
        maximumSelectionLength: 10
        // ajax: {
        //     delay: 100,
        //     url: 'http://api.dataatwork.org/v1/skills/autocomplete',
        //     dataType: 'json',
        //     data: function (params) {
        //         return {
        //             contains: encodeURI(params.term)
        //         };
        //     },
        //     processResults: function (data) {
        //         return {
        //             results: $.map(data, function (obj) {
        //                 obj.id = obj.uuid;
        //                 obj.text = obj.suggestion;
        //                 return obj
        //             })
        //         };
        //     }
        // }
    });
});