(function(){

    var numberMap = {
        next: 1,
        one: 1,
        two: 2,
        three: 3,
        four: 4,
        five: 5,
        six: 6
    };

    var weekMap = {
        day: 1,
        week: 2
    };

    // the promise form
    $('.promise-form').submit(function(e) {
        e.preventDefault();

        var promiseInput = $('#id_text'),
            promise = promiseInput.val();

        if (promise) {

            // naive natural language processing
            var mPromise = promise.match(/(\w+)\s*(week|day)\s*/i);

            if (mPromise) {
                var value = mPromise[1],
                    unit = mPromise[2];

                if (isFinite(value)) {
                    value = parseInt(value, 10);
                } else {
                    value = parseInt(numberMap[value.toLowerCase()] || 0, 10);
                }

                if (value && value < 7) {
                    $('#promise-duration-value').val(value);
                }

                unit = unit.toLowerCase();
                $('#promise-duration-unit').val(weekMap[unit]);
            }

            $('#promise-modal').modal('show');
        } else {
            var controlGroup = $(this);
            promiseInput.focus();

            controlGroup.addClass('error');
            setTimeout(function() {
                controlGroup.removeClass('error');
            }, 1600);
        }
    });

}());