last_message_id = -1;

        function get_alliance_messages(){
            alliance_text_area = document.getElementById("alliance_text_area");
            $.get('/game/get_alliance_messages/',{'last_message_id':last_message_id}, function(data){

                messages = data.split('$$');
                for(i=0; i < messages.length; i++){
                    if(messages[i] != ""){
                        real_message = messages[i].split('||');
                        message_id = parseInt(real_message[0]);
                        if(message_id>last_message_id){
                            last_message_id=message_id;
                        }
                        alliance_text_area.value += real_message[1]+': '+real_message[2]+'\n'
                        alliance_text_area.scrollTop = alliance_text_area.scrollHeight;
                    }
                }
            });
        }

        function sendAllianceMessage() {
            var x = document.getElementById("user_msg").value;
            $.get('/game/add_alliance_message/', {'message': x,'to_alliance_id':{{acc.alliance.pk}}}, function(data){
                if(data == -1){
                    $('#requestResult').html("Message was not delivered");
                    $("#leaveNotifAlert").show();
                }else{
                    document.getElementById("user_msg").value="";
                    get_alliance_messages();
                }
            });
        }

        function sendAllianceRequest() {
            var x = document.getElementById("msg").value;
            $.get('/game/alliance_request/{{ alliance.name}}', {msg: x}, function(data){
                $('#requestResult').html(data);
                if(data != -1){
                    $("#leaveNotifAlert").show();
                }
            });
            document.getElementById("msg").value="";
        }

        function leaveAlliance() {
            $.get('/game/leave_alliance/', function(data){
                $('#requestResult').html(data);
                if(data != -1){
                    $("#leaveNotifAlert").show();
                }
            });
        }

        function changeOrders() {
            var orders = document.getElementById("orders_text_area").value;
            $.get('/game/change_orders/',{'orders':orders}, function(data){
                $('#requestResult').html("Orders Changed Successfully");
                if(data != -1){
                    $("#leaveNotifAlert").show();
                }
            });
        }

        function returnToGame(){
            window.location.href = "/game/";
        }

		$(document).ready(function(){

            {% if acc.alliance == alliance %}
                {% if request.user.username != leader %}
                    document.getElementById("orders_text_area").readOnly = true;
                {% endif %}
            {% endif %}

            $('.acceptButton').click(function() {
                reqAcc = $(this).attr("reqAcc");
                $.get('/game/accept_alliance/'+reqAcc, function(data){
                    location.reload();
                });
            });

            $('.declineButton').click(function() {
                reqAcc = $(this).attr("reqAcc");
                $.get('/game/decline_alliance/'+reqAcc, function(data){
                    location.reload();
                });
            });

            $('.kickButton').click(function() {
                reqAcc = $(this).attr("reqAcc");
                $.get('/game/kick_member/'+reqAcc, function(data){
                    console.log(data);
                    if(data == 1){
                        location.reload();
                    }
                });
            });

            $('.alert .close').on('click', function(e) {
                returnToGame();
            });

            $('#sendButton').click(function(){
                sendAllianceMessage();
            });

            $('#user_msg').keyup(function(event){
                if(event.keyCode == 13){
                    $("#sendButton").click();
                }
            });

            document.getElementById("alliance_text_area").readOnly = true;

            //polling that gets the messages
            get_alliance_messages();
            setInterval(function() {get_alliance_messages()}, 1000);
        });