function update() {
    $.ajax({
        url: 'ajax/emailupdate/',
        dataType: 'json',
        success: function(data) {
            num = data.length;
            for (var i = 0; i < num; i++) {
                $('#content').append(`
                    <div name = '`+data[i][7]+`'>
                    <input onclick = 'check(this)' id = '`+i+`check' type = 'checkbox' name = '`+data[i][7]+`' class = 'checkbox'>
                    <img src = '/static/emails/trash.png' class = 'trash' id = '`+i+`trash' onclick = 'deleter(this)' name = '`+data[i][7]+`''>
                    <div class = 'cont_element' id = '`+i+`' onclick = 'displayemail(this)' name = '`+data[i][7]+`'>
                        <div class = 'name'>
                            <p>`+data[i][4]+`</p>
                        </div>
                        <div class = 'subject'>
                            <p>`+data[i][1]+`</p>
                        </div>
                        <div class = 'date'>
                            <p>`+data[i][2]+`</p>
                        </div>
                    </div>
                    <div class = 'email' id = '`+i+`frame' name = '`+data[i][7]+`'>
                        <div class = 'emailadd'>
                            <p>From: `+data[i][5]+`<p>
                            <p>To: vegautam@gmail.com<p>
                            <p>Subject: `+data[i][1]+`</p>
                        </div>
                        <div class = 'cont'>
                        `+data[i][0]+`
                        </html>
                        </div>
                    </div>
                    </div>
                    `)
            }
        }


    })
}

var trash = []
function check(ele) {
    let id = ele.id;
    var content = document.getElementById(id)
    if (content.checked) {
        trash.push(id);
    }
    else if (!content.checked) {
        var index = trash.indexOf(id);
        if (index != -1) {
            trash.splice(index, 1);
        }
    }
}

function deleter(ele) {
    $.ajax({
        url: 'ajax/emaildelete/',
        type: 'post',
        data: {name : ele.name}
    });
    $('#content').html("")
    update()
}

function displayemail(ele) {
    let id = ele.id;
    var x = document.getElementsByClassName('email');
    for (var i = 0; i < x.length; i++) {
        x[i].style.display = 'none';
    }
    document.getElementById(id + 'frame').style.display = 'block';
    document.getElementById(id).setAttribute("onclick", 'hideemail(this)');
}

function hideemail(ele) {
    id = ele.id
    document.getElementById(id + 'frame').style.display = 'none'
    document.getElementById(id).setAttribute('onclick', 'displayemail(this)')
}