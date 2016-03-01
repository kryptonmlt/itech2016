        var latest_log_id = -1;

        function populateLogBox(){
            logs_text_area = document.getElementById("logs_text");
            $.get('/game/get_logs/',{'latest_log_id':latest_log_id}, function(data){

                logs = data.split('$$');
                for(i=0; i < logs.length; i++){
                    if(logs[i] != ""){
                        real_log = logs[i].split('||');
                        log_id = parseInt(real_log[0]);
                        if(log_id>latest_log_id){
                            latest_log_id=log_id;
                        }
                        logs_text_area.value += real_log[1]+': '+real_log[2]+'\n'
                        logs_text_area.scrollTop = logs_text_area.scrollHeight;
                    }
                }
            });
        }

        function updateResources(){
            $.get('/game/get_resources/', function(data){
                resources = data.split(',');
                $('#goldSpan').html(resources[0]);
                $('#lumberSpan').html(resources[1]);
                $('#stonesSpan').html(resources[2]);
            });
        }

        function getBuildingInfo(data){
            index = data.indexOf(",");
            var info = [data.substr(0, index), data.substr(index + 1)];
            return info;a
        }

        function startTimer(duration, display) {
            var timer = duration, minutes, seconds;
            var ct = setInterval(function () {
                minutes = parseInt(timer / 60, 10);
                seconds = parseInt(timer % 60, 10);

                minutes = minutes < 10 ? "0" + minutes : minutes;
                seconds = seconds < 10 ? "0" + seconds : seconds;

                display.textContent = minutes + ":" + seconds;

                if (--timer < 0) {
                    clearInterval(ct);
                    collectTimer();
                }
            }, 1000);
        }

        function stopTimer(){

        }

        function collectTimer(){
            display = document.querySelector('#timeSpan');
            $.get('/game/collect', function(data){
                if(data != "-1"){
                    var res = data.split(",");
                    if(res[0] == "DONE"){
                        display.textContent="Ready! ";
                        document.getElementById("collectButton").disabled = false;
                    }else{
                        var wholeMin = res[1].split(".");
                        minutes = parseInt(wholeMin[0]);
                        startTimer(minutes, display);
                        document.getElementById("collectButton").disabled = true;
                    }
                }
            });
        }


		$(document).ready(function(){
		    document.getElementById("logs_text").readOnly = true;

            $('#housesButton,#cavesButton,#minesButton,#millsButton,#wallButton,#footmenButton,#knightsButton,#bowmenButton,#war_machinesButton,#farmsButton').click(function(){
                et = $(this).attr("element_type");
                $.get('/game/buy', {element_type: et}, function(data){
                    if(data == "-1"){
                        //show alert
                        $("#alertNoGold").show();
                    }else if (data=="-2"){
                    	//show alert
                        $("#alertNoLumber").show();
                    }else if (data=="-3"){
                    	//show alert
                        $("#alertNoStones").show();
                    }else if (data=="-4"){
                    	//show alert
                        $("#alertInsufficientMaxTroops").show();
                    }else {
                       //increments stuff
                       switch(et){
                           case "farms":
                                console.log(data)
                                var res = data.split(",");
                                $('#farms').html(res[0]);
                                $('#maximumTroops').html(res[1]);
                                $('#farms_cost').html(res[2]+","+res[3]+","+res[4]);
                                try {
                                    $.get('/game/city_img/'+res[0], function(data){
                                        if(data!=-1){
                                            document.getElementById("cityImg").src = data;
                                        }
                                    });
                                }
                                catch(err) {
                                    console.log(err.message);
                                }
                                break;
                           case "wall":
                                console.log(data);
                                var res = getBuildingInfo(data);
                                $('#wallLevel').html(res[0]);
                                $('#wallCost').html(res[1]);
                                break;
                           case "stone_caves":
                                var res = getBuildingInfo(data);
                                $('#stone_caves').html(res[0]);
                                $('#stone_caves_cost').html(res[1]);
                                break;
                           case "gold_mines":
                                var res = getBuildingInfo(data);
                                $('#gold_mines').html(res[0]);
                                $('#gold_mines_cost').html(res[1]);
                                break;
                           case "lumber_mills":
                                var res = getBuildingInfo(data);
                                $('#lumber_mills').html(res[0]);
                                $('#lumber_mills_cost').html(res[1]);
                                break;
                           case "knights":
                                $('#knights').html(data);
                                break;
                           case "footmen":
                                $('#footmen').html(data);
                                break;
                           case "bowmen":
                                $('#bowmen').html(data);
                                break;
                           case "knights":
                                $('#knights').html(data);
                                break;
                           case "war_machines":
                                $('#war_machines').html(data);
                                break;
                       }
                       updateResources();
                   }
                 });
            });

            $('#createAllianceButton').click(function(){
                name=document.getElementById("createAllianceName").value;
                desc=document.getElementById("createDescName").value;
                $.get('/game/create_alliance', {'name': name,'desc':desc}, function(data){
                    if(data ==1){
                        window.location.href = "/game/";
                    }else{
                        console.log(data);
                    }
                });
            });

            $('#collectButton').click(function(){
                document.getElementById("collectButton").disabled = true;
                collectTimer();
                updateResources();
            });


            // when alert close
            $('.alert .close').on('click', function(e) {
                $(this).parent().hide();
            });

            //polling that gets the logs
            populateLogBox();
            setInterval(function() {populateLogBox()}, 5000);

            collectTimer();
        });