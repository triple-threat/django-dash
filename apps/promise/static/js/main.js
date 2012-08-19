(function(){

    (function() {
        // promise form
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
            day: 'days',
            week: 'weeks'
        };

        $('.visible-promise-input').focus();

        // the promise form
        $('.promise-form').submit(function(e) {
            e.preventDefault();

            var promiseInput = $('.visible-promise-input'),
                promise = promiseInput.val();

            if (promise) {
                // naive natural language processing
                var mPromise = promise.match(/(\w+)\s+(week|day)\s*/i),
                    durationValueSelect = $('#id_duration_value');

                if (mPromise) {
                    var value = mPromise[1],
                        unit = mPromise[2];

                    if (isFinite(value)) {
                        value = parseInt(value, 10);
                    } else {
                        value = parseInt(numberMap[value.toLowerCase()] || 0, 10);
                    }

                    if (value && value < 7) {
                        durationValueSelect.val(value);
                    }

                    unit = unit.toLowerCase();
                    $('#id_duration_unit').val(weekMap[unit]);
                }

                $('.invisible-promise-input').val(promise);
                $('#promise-modal').modal('show');

                // the fact that the input is not on the page
                // makes it impossible to be focused
                // delayoing the focus
                setTimeout(function() {
                    durationValueSelect.focus();
                }, 200);

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

    // the navigation
    // activated the home link if you are on it
    $('.navbar a[href="'+ location.pathname +'"]').parent('li').addClass('active');

    // feed tabs
    (function() {

        // activating the current tab
        var feedTabs = $('.feed-tabs');
        var activeLink = feedTabs.find('a[href$="'+ location.search +'"]');
        if (!activeLink.length) {
            activeLink = feedTabs.find('.default');
        }
        activeLink.parent('li').addClass('active');

        var promiseFeedContent = $('#promise-feed-content');
        feedTabs.on('click', 'a', function(e) {
            e.preventDefault();

            var link = $(this);

            feedTabs.find('> li').removeClass('active');
            link.parent('li').addClass('active');

            var url = link.attr('href');

            feedTabs.addClass('loading');
            $.ajax({
                url: url,
                success: function(response) {
                    promiseFeedContent.html(response);
                    feedTabs.removeClass('loading');
                }
            });
        });
        
    }());

}());
