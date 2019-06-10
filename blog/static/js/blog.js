$('#commentForm').submit(function (event) {
    //停止正常的form请求
    event.preventDefault();
    // var f = $('#commentForm');
    var text = $('.text-txt').val();
    var url = $('#commentForm').attr('action');
    // var csrfmiddlewaretoken = f.find("input[name='csrfmiddlewaretoken']").attr('value');
    var csrfmiddlewaretoken = $("#commentForm input[name='csrfmiddlewaretoken']").attr('value');
    $.post(url, {'text': text, 'parent': -1, 'csrfmiddlewaretoken': csrfmiddlewaretoken}, function (data) {
        if (data.code === 0) {
            $('#result').removeClass('hidden').html(data.message)
        } else if (data.code === 2) {
            alert(data.message);
            window.location.reload();
        } else {
            var new_comment = $('.media:first-child').clone(true);
            new_comment.find('#ctext').html(data.cur_comment.ctext);
            new_comment.find('.media-body .text-right span').html(data.cur_comment.ctime);
            new_comment.find('.media-heading:first-child').addClass('user-id', data.cur_comment.uid);
            new_comment.find('.media-heading:first-child a').html(data.cur_comment.uname);
            new_comment.attr('data-id', data.cur_comment.cid).prependTo('.comments-content');
        }
    })
});

var curr_show_comment_form_id;

function show_comment_form(event) {
    var id;
    var comment_id =$(event.target).attr('comm_id');
    var sub_html = `<div class="comments-form"><textarea id="sub_comment_text" cols="80" rows="5" placeholder="\u8bf7\u81ea\u89c9\u9075\u5b88\u4e92\u8054\u7f51\u76f8\u5173\u7684\u653f\u7b56\u6cd5\u89c4\\uff0c\u4e25\u7981\u53d1\u5e03\u8272\u60c5\u3001\u66b4\u529b\u3001\u002a\u5c4f\u853d\u7684\u5173\u952e\u5b57\u002a\u7684\u8a00\u8bba\u3002" style="float: left;width: 85%"></textarea><button class="mybtn" id="addComment" style="float: right;">\u53d1\u8868\u8bc4\u8bba</button></div>`;
    if ($(event.target).attr('parent_id')) {
        id = $(event.target).attr('parent_id');
    } else {
        id = comment_id;
    }
    if (!(curr_show_comment_form_id === id)) {
        $(('#sub_content_' + id)).removeClass('hidden').html(sub_html);
        curr_show_comment_form_id = id;
    }

    $('#addComment').on('click', function (event) {
        var text = $(event.target).parent().find('textarea').val();
        var url = $('#commentForm').attr('action');
        var csrfmiddlewaretoken = $("#commentForm input[name='csrfmiddlewaretoken']").attr('value');

        $.post(url, data = {
            'text': text,
            'parent': comment_id,
            'csrfmiddlewaretoken': csrfmiddlewaretoken
        }, function (data) {
            alert(data.message);
            window.location.reload();
        });
    });
}

$('.showSubCommentForm').on('click', show_comment_form);

$('body').on('DOMNodeInserted', function () {
    if (curr_show_comment_form_id)
        $('#sub_content_' + curr_show_comment_form_id).addClass('hidden').html("");
});


$('#toLogin').click(function () {
    $('#login_modal .modal-body').load('/accounts/login/');
    $('#login_modal').modal()
});

$('#login_submit').click(function () {
    // $('#login_submit').unbind();
    $('#loginForm').unbind().submit(function (event) {
        event.preventDefault();
        var url = $('#loginForm').attr('action');
        var username = $('#id_username').val();
        var password = $('#id_password').val();
        var csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").attr('value');
        $.post(url, {
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': csrfmiddlewaretoken
        }, function (data) {
            if (data.code === 1) {
                alert(data.message);
                window.location.reload()
            } else {
                $('#login_message').removeClass('hidden').html(data.message)
            }
        })
    });
    $('#loginSubmit').click();
});


$('#toReg').click(function () {
    $('#reg_modal .modal-body').load('/accounts/register/');
    $('#reg_modal').modal()
});

// $('#reg_submit').unbind();
$('#reg_submit').click(function () {

    $('#regForm').unbind().submit(function (event) {
        event.preventDefault();
        var url = $('#regForm').attr('action');
        var username = $('#id_username').val();
        var email = $('#id_email').val();
        var password1 = $('#id_password1').val();
        var password2 = $('#id_password2').val();
        var csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").attr('value');
        var data = {
            'username': username,
            'email': email,
            'password1': password1,
            'password2': password2,
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
        };
        $.post(url, data, function (data) {
            if (data.code === 1) {
                alert(data.message);
                window.location.reload()
            } else {
                if (data.form) {
                    var error = '';
                    for (var k in data.form) {
                        for (var v in data.form[k]) {
                            error += data.form[k][v]
                        }
                    }
                    $('#reg_message').removeClass('hidden').html(error)
                } else {
                    $('#reg_message').removeClass('hidden').html(data.message)
                }

            }
        });
    });

    $('#regSubmit').click();
});

$('#toModify').click(function (event) {
    event.preventDefault();
    var url = $(event.target).attr('href');
    $.get(url, function (data) {
        if (data.code === 1){
            $('#modify_modal').modal()
        }
    });


});

$('#toPwdChange').click(function (event) {
    event.preventDefault();
    var url = $(event.target).attr('href');
    $('#modify_modal .modal-body').load(url,function () {
        $('#pwdChangeSubmit').click(function (data) {
            if (data.code === 1){
                alert(data.message)
            } else{
                alert(data.message)
            }
        })
    });
});

function load_comment(event) {
    event.preventDefault();
    var url = $(event.target).attr('href');
    $('#comment_list').load(url, function (event) {
        $('.load_page').on('click', load_comment);
        $('.showSubCommentForm').on('click', show_comment_form);
    });

}


$('.load_page').on('click', load_comment);