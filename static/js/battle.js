 last_message_id = -1;

        function get_messages(){
            message_text_area = document.getElementById("message_text_area");
            $.get('/game/get_messages/',{'last_message_id':last_message_id,'to_account_id':enemyId},

            function(data){
                messages = data.split('$$');
                for(i=0; i < messages.length; i++){
                    if(messages[i] != ""){
                        real_message = messages[i].split('||');
                        message_id = parseInt(real_message[0]);
                        if(message_id>last_message_id){
                            last_message_id=message_id;
                        }
                        message_text_area.value += real_message[1]+': '+real_message[2]+'\n'
                        message_text_area.scrollTop = message_text_area.scrollHeight;
                    }
                }
            });
        }

        function sendMessage() {
            var x = document.getElementById("user_msg").value;
            $.get('/game/add_message/', {'message': x,'to_account_id':enemyId}, function(data){
                if(data == -1){
                    $('#notif_span').html("Message was not delivered");
                    $("#notif_alert").show();
                }else{
                    document.getElementById("user_msg").value="";
                    get_messages();
                }
            });
        }

        function startAttackTimer(duration, display) {
            var timer = duration, minutes, seconds;
            var ct = setInterval(function () {
                minutes = parseInt(timer / 60, 10);
                seconds = parseInt(timer % 60, 10);

                minutes = minutes < 10 ? "0" + minutes : minutes;
                seconds = seconds < 10 ? "0" + seconds : seconds;

                display.textContent = minutes + ":" + seconds;

                if (--timer < 0) {
                    clearInterval(ct);
                    attackTimer();
                }
            }, 1000);
        }

        function attackTimer(){
            display = document.querySelector('#attackTimerSpan');
            $.get('/game/last_attacked/'+enemyId, function(data){
                if(data != "-1"){
                    var res = data.split(",");
                    if(res[0] == "DONE"){
                        display.textContent="Ready! ";
                        document.getElementById("attackButton").disabled = false;
                    }else{
                        var wholeMin = res[1].split(".");
                        minutes = parseInt(wholeMin[0]);
                        startAttackTimer(minutes, display);
                        document.getElementById("attackButton").disabled = true;
                    }
                }
            });
        }

        $(document).ready(function(){
            attackTimer();
        	logs_text_area = document.getElementById("logs_text");

            $('#attackButton').click(function(){
                document.getElementById("attackButton").disabled = true;
          	    $.get('/game/attack/'+enemyUsername, function(data){
                    console.log(data);
                    logs_text_area.value +=data
                    logs_text_area.scrollTop = logs_text_area.scrollHeight;
                    attackTimer();
                });
            });

            document.getElementById("message_text_area").readOnly=true;
            $('#sendButton').click(function(){
                sendMessage();
            });

            $('#user_msg').keyup(function(event){
                if(event.keyCode == 13){
                    $("#sendButton").click();
                }
            });

            $('.alert .close').on('click', function(e) {
                $(this).parent().hide();
            });

            //polling that gets the messages
            get_messages();
            setInterval(function() {get_messages()}, 1000);
        });
