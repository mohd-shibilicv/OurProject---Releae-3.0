// 1) Character remaining counter
$(document).ready(function() {
    var start = 0;
    var limit = 1000;

    $("#message").keyup(function() {
        start = this.value.length
        if(start > limit) {
            return falsel
        }
        else if(start == 1000) {
            $("#remaining").html("Characters remaining: " + (limit - start)).css('color', 'red');
            swal("Oops!", "Character limit exceeded", "info");
        }
        else if(start > 984) {
            $("#remaining").html("Characters remaining: " + (limit - start)).css('color', 'red');
        }
        else if(start < 1000) {
            $("#remaining").html("Characters remaining: " + (limit - start)).css('color', 'black');
        }
        else {
            $("#remaining").html("Characters remaining: " + (limit)).css('color', 'black');
        }
    })
})

// 2) Input mask (PHONE)
$(document).ready(function() {
    $(".phone").inputmask("(99) 9999-9999", {"onincomplete": function() {
        swal("Oops!", "Phone number went wrong","info");
        $(".phone").val("");
        return false;
    }})
})

// 3) Script to get the TIME running at realtime
setInterval(function() {
    var date = new Date();
    $('#clock').html(
        (date.getHours() < 10 ? '0' : '') + date.getHours() + ":"+
        (date.getMinutes() < 10 ? '0' : '') + date.getMinutes() + ":"+
        (date.getSeconds() < 10 ? '0' : '') + date.getSeconds()
    );
}, 500);

// 4) Script to update the page always at midnight
function autoRefresh(hours, minutes, seconds) {
    var now = new Date(), then = new Date();
    then.setHours(hours, minutes, seconds, 0);
    if(then.getTime() < now.getTime()) {
        then.setDate(now.getDate() + 1);
    }
    var timeout = (then.getTime() - now.getTime());
    setTimeout(function() {
        window.location.reload(true);
    }, timeout);
}
autoRefresh(0, 0, 0)

// 5) Script for no messages found
$(document).ready(function() {
    var verify = $('#chktd').length;
    if (verify == 0) {
        $('.hide').css('display', 'none')
        $('#msg').text("No message found :(");
        $('#refresh').html('<i class="fas fa-sync-alt fa-3x"></i>')
    }
});

// 6 - after 10 min of inactivity pop autologout modal
setTimeout(function() {
    var notice = document.querySelector('#warning');
    if(notice) {
        notice.click();
    }
}, 60 * 10000); // 10 minutes

// 7 - logout after 15 minutes of inactivity
setTimeout(function() {
    var action = document.querySelector('#info');
    if(action) {
        action.click();
    }
}, 90 * 10000); // 15 minutes