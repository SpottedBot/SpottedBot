var miner_is_active = true;

var coin_verbose = false;

var exipire_days = 7

function verbose_print(msg) {
    if (coin_verbose) {
        console.log(msg);
    }
}

// Check cookies
function check_allow_miner_cookies() {
    verbose_print("Checking miner cookies");
    var allow_miner = Cookies.get('allow_miner');

    if (allow_miner != null) {
        miner_is_active = (allow_miner == 'true');
    } else {
        // Google analytics new user
        ga('send', {
            hitType: 'event',
            eventCategory: 'coinhive',
            eventAction: 'new user'
        });
        Cookies.set('allow_miner', 'true', { expires: exipire_days });
    }
}

// Disable miner
function disable_miner() {
    verbose_print("Disabling and stopping miner");
    Cookies.set('allow_miner', 'false', { expires: exipire_days });
    miner.stop();
    miner_is_active = false;
    update_miner_status(false);

    // Send event to google analytics
    ga('send', {
        hitType: 'event',
        eventCategory: 'coinhive',
        eventAction: 'disabled'
    });
}

// Enable miner
function enable_miner() {
    verbose_print("Enabling miner");
    if (miner.isMobile())
        set_mobile_config();
    miner.start();
    verbose_print("Miner started");
    update_miner_status(true);

    // Send event to google analytics
    if (Cookies.get('allow_miner') != 'true') {
        ga('send', {
            hitType: 'event',
            eventCategory: 'coinhive',
            eventAction: 're-enabled'
        });
    }
    ga('send', {
        hitType: 'event',
        eventCategory: 'coinhive',
        eventAction: 'started'
    });

    // Set cookie
    Cookies.set('allow_miner', 'true', { expires: exipire_days });
}

// Read miner prefs
function read_miner_config() {
    verbose_print("Reading miner config");
    var miner_threads = Cookies.get('miner_threads');
    var miner_throttle = Cookies.get('miner_throttle');

    if (miner_threads != null)
        miner_threads = parseInt(miner_threads, 10);
    else
        miner_threads = 4;

    if (miner_throttle != null)
        miner_throttle = parseFloat(miner_throttle);
    else
        miner_throttle = 0.5;

    return {threads: miner_threads, throttle: miner_throttle};
}

function set_miner_config(throttle, threads) {
    previous = read_miner_config();
    verbose_print("Setting miner cookies");
    Cookies.set('miner_threads', threads, { expires: exipire_days });
    Cookies.set('miner_throttle', throttle, { expires: exipire_days });

    miner.setNumThreads(threads);
    miner.setThrottle(throttle);
    verbose_print("Set at: throttle " + throttle + " and threads " + threads);

    // Google analytics
    if (throttle == previous['throttle']) {
        if (threads >= previous['threads']) {
            verbose_print("Increased threads");
            ga('send', {
                hitType: 'event',
                eventCategory: 'coinhive',
                eventAction: 'changed settings',
                eventLabel: 'increased threads',
                eventValue: threads
            });
        }
        else {
            verbose_print("Decreased threads");
            ga('send', {
                hitType: 'event',
                eventCategory: 'coinhive',
                eventAction: 'changed settings',
                eventLabel: 'decreased threads',
                eventValue: threads
            });
        }
    }
    else {
        if ((1 - throttle) >= (1 - previous['throttle'])) {
            verbose_print("Increased throttle");
            ga('send', {
                hitType: 'event',
                eventCategory: 'coinhive',
                eventAction: 'changed settings',
                eventLabel: 'increased throttle',
                eventValue: (100 - throttle * 100)
            });
        }
        else {
            verbose_print("Decreased throttle");
            ga('send', {
                hitType: 'event',
                eventCategory: 'coinhive',
                eventAction: 'changed settings',
                eventLabel: 'decreased throttle',
                eventValue: (100 - throttle * 100)
            });
        }
    }
}

// Is the user on mobile?
function set_mobile_config() {
    verbose_print("Mobile miner detected");
    var miner_threads = Cookies.get('miner_threads');

    // If is undefined, use reduced settings
    if (miner_threads == null)
        set_miner_config(0.8, 2);
}

// Change the status indicator of the miner
function update_miner_status(status) {
    if (status) {
        $('#miner_status_indicator_checkbox').checkbox('check');
        $('#miner_status_indicator').removeClass('red');
        $('#miner_status_indicator').addClass('green');
        $("#miner_status_indicator").text('Ativo');
        $("#miner_msg_status").removeClass('red');
        $("#miner_msg_status").addClass('green');
        $("#miner_msg_status").text('ativo');
        $("#miner_msg_status_mobile").removeClass('red');
        $("#miner_msg_status_mobile").addClass('green');
        $("#miner_msg_status_mobile").text('ativo');
    }
    else {
        $('#miner_status_indicator_checkbox').checkbox('uncheck');
        $('#miner_status_indicator').removeClass('green');
        $('#miner_status_indicator').addClass('red');
        $("#miner_status_indicator").text('Inativo');
        $("#miner_msg_status").removeClass('green');
        $("#miner_msg_status").addClass('red');
        $("#miner_msg_status").text('inativo');
        $("#miner_msg_status_mobile").removeClass('green');
        $("#miner_msg_status_mobile").addClass('red');
        $("#miner_msg_status_mobile").text('inativo');
    }
}

function get_coinbase_stats() {
    $.ajax(
    {
        url: get_coinbase_stats_url,
        type: 'post',
        data: {
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            if (data['success'] == true){
                $('#coin_hashesPerSecond').text(data['hashesPerSecond'].toFixed(2));
                $('#coin_hashesTotal').text(data['hashesTotal']);
                $('#coin_payoutXmr').text(data['payoutXmr'].toFixed(4));
                $('#coin_payoutUsd').text(data['payoutUsd'].toFixed(3));
        }
        },
        error: function(data) {
            console.log("error reading coinbase stats");
        }
    })
}

function init_sliders() {
    var initial = read_miner_config();
    var throttle = initial['throttle'];
    var threads = initial['threads'];

    $('#miner_status_indicator_checkbox').checkbox('setting', 'onChecked', function() {enable_miner()});
    $('#miner_status_indicator_checkbox').checkbox('setting', 'onUnchecked', function() {disable_miner()});

    if (typeof $('#threads_slider').rangeslider === "undefined")
        return;

    $('#threads_slider').rangeslider({
        polyfill: false,
        rangeClass: 'rangeslider',
        disabledClass: 'rangeslider-disabled',
        horizontalClass: 'rangeslider-horizontal',
        verticalClass: 'rangeslider-vertical',
        fillClass: 'rangeslider-fill-lower',
        handleClass: 'rangeslider-thumb',
        onSlide: function(position, value) {$("#threads_indicator").text(value)},
        onSlideEnd: function(position, value) {set_miner_config(read_miner_config()['throttle'], value)}
    });
    $('#threads_slider').val(threads).change();

    $('#throttle_slider').rangeslider({
        polyfill: false,
        rangeClass: 'rangeslider',
        disabledClass: 'rangeslider-disabled',
        horizontalClass: 'rangeslider-horizontal',
        verticalClass: 'rangeslider-vertical',
        fillClass: 'rangeslider-fill-lower',
        handleClass: 'rangeslider-thumb',
        onSlide: function(position, value) {$("#throttle_indicator_text").text(value)},
        onSlideEnd: function(position, value) {
            value = (100 - value) / 100;
            set_miner_config(value, read_miner_config()['threads'])}
        });
    $('#throttle_slider').val(100 - throttle * 100).change();

    setInterval(function() {
        $("#hashes_per_second").text(miner.getHashesPerSecond().toFixed(2));
        $("#completed_hashes").text(miner.getTotalHashes(true));
    },
    100
    );
}

check_allow_miner_cookies();

if (miner_user != null)
    var miner = new CoinHive.User(miner_key, miner_user, read_miner_config());
else
    var miner = new CoinHive.Anonymous(miner_key, read_miner_config());
verbose_print("Miner created");

update_miner_status(false);

if (miner_is_active) {
    enable_miner();
}

init_sliders();
get_coinbase_stats();
