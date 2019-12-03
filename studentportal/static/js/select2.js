$(document).ready(function () {
    $('.select2-skills').select2({
        tags: true,
        maximumSelectionLength: 10
    });

    $('.select2-dropdown').select2({});

    var $modulesSelect2 = $('.select2-modules');
    $modulesSelect2.select2({
        minimumInputLength: 3,
        placeholder: 'Search modules...',
        ajax: {
            delay: 50,
            url: '/api/1.0/modules/autocomplete',
            dataType: 'json',
            data: function (params) {
                var query = {
                    search: params.term,
                    page: params.page || 1
                };
                return query;
            },
            processResults: function (data, params) {
                return {
                    results: $.map(data, function (obj) {
                        obj.id = obj._id;
                        obj.text = obj._id + ' - ' + obj.module_title;
                        return obj
                    }),
                    pagination: {
                        more: (params.page * 10) < data.count_filtered
                    }
                };
            }
        }
    });

    $modulesSelect2.on('select2:select', function (e) {
        var data = e.params.data;
        window.location.href = "/module/" + data.id;
    });
});