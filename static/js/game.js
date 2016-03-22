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
                $('#totalTroops').html(resources[0]);
                $('#goldSpan').html(resources[1]);
                $('#lumberSpan').html(resources[2]);
                $('#stonesSpan').html(resources[3]);
            });
        }

         function updateOpponentsList(){
            $.get('/game/updateEnemies/', function(data){
                users = data.split(',');
                oppHtml="";
                for(i=0; i<users.length;i++){
                    oppHtml+="<a href=\"/game/battle/"+users[i]+"\" class=\"list-group-item\"><strong>"+users[i]+"</strong></a>";
               }
                $('#opponents_list').html(oppHtml);
            });
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
                    collectTimer("false");
                }
            }, 1000);
        }

        function collectTimer(auto){
            display = document.querySelector('#timeSpan');
            $.get('/game/remaining_collect', function(data){
                if(data != "-1"){
                    var res = data.split(",");
                    if(res[0] == "DONE"){
                        display.textContent="Ready! ";
                        document.getElementById("collectButton").disabled = false;
                        if(auto == "true"){
                            $.get('/game/collect', function(data){
                                collectTimer("false")
                                updateResources();
                            });
                        }
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

            collectTimer("false");
		    document.getElementById("logs_text").readOnly = true;

            $('#housesButton,#cavesButton,#minesButton,#millsButton,#wallButton,#footmenButton,#knightsButton,#bowmenButton,#war_machinesButton,#farmsButton').click(function(){
                et = $(this).attr("element_type");
                $.get('/game/buy', {element_type: et}, function(data){
                    if(data == "-1"){
                        //show alert
                        $(".modal_overlay").fadeIn("fast");
                        $(".modal_content_gold").fadeIn("fast");
                    }else if (data=="-2"){
                    	//show alert
                        $(".modal_overlay").fadeIn("fast");
                        $(".modal_content_lumber").fadeIn("fast");
                    }else if (data=="-3"){
                    	//show alert
                        $(".modal_overlay").fadeIn("fast");
                        $(".modal_content_stone").fadeIn("fast");
                    }else if (data=="-4"){
                    	//show alert
                        $(".modal_overlay").fadeIn("fast");
                        $(".modal_content_supply").fadeIn("fast");
                    }else {
                       //increments stuff
                       switch(et){
                           case "farms":
                                console.log(data)
                                var res = data.split(",");
                                $('#farms').html(res[0]);
                                $('#maximumTroops').html(res[1]);
                                $('#farms_gold_cost').html(res[2]);
                                $('#farms_lumber_cost').html(res[3]);
                                $('#farms_stone_cost').html(res[4]);
                                getMap();
                                updateOpponentsList();
                                break;
                           case "wall":
                                console.log(data);
                                var res = data.split(",");
                                $('#wallLevel').html(res[0]);
                                $('#walls_gold_cost').html(res[1]);
                                $('#walls_lumber_cost').html(res[2]);
                                $('#walls_stone_cost').html(res[3]);
                                getMap();
                                break;
                           case "stone_caves":
                                var res = data.split(",");
                                $('#stone_caves').html(res[0]);
                                $('#stone_mine_gold_cost').html(res[1]);
                                $('#stone_mine_lumber_cost').html(res[2]);
                                $('#stone_mine_stone_cost').html(res[3]);
                                getMap();
                                break;
                           case "gold_mines":
                                var res = data.split(",");
                                $('#gold_mines').html(res[0]);
                                $('#gold_mine_gold_cost').html(res[1]);
                                $('#gold_mine_lumber_cost').html(res[2]);
                                $('#gold_mine_stone_cost').html(res[3]);
                                getMap();
                                break;
                           case "lumber_mills":
                                var res = data.split(",");
                                $('#lumber_mills').html(res[0]);
                                $('#lumber_mill_gold_cost').html(res[1]);
                                $('#lumber_mill_lumber_cost').html(res[2]);
                                $('#lumber_mill_stone_cost').html(res[3]);
                                getMap();
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
                        if(data == "-1"){
                            //show alert
                            $(".modal_overlay").fadeIn("fast");
                            $(".modal_content_noalliname").fadeIn("fast");
                        }else if (data=="-2"){
                            //show alert
                            $(".modal_overlay").fadeIn("fast");
                            $(".modal_content_allinameexists").fadeIn("fast");
                        }
                    }
                });
            });

            $('#collectButton').click(function(){
                document.getElementById("collectButton").disabled = true;
                collectTimer("true");
            });

            $('#findMeButton').click(function(){
                initializeMapWithPlayerLoc();
            });

            // when alert close
            $('.alert .close:not(.closeModal').on('click', function(e) {
                $(this).parent().hide();
            });

            // when alert close
            $('.close.closeModal').on('click', function(e) {
                $(this).closest('.modal_overlay').hide();
                $(this).closest('.modal_content').hide();
            });

            $(".modal_content").on('click', function(e){
                e.preventDefault();
                return false;
            });

            $(".modal_overlay").on('click', function(e){
                $(this).closest('.modal_overlay').hide();
                $(this).closest('.modal_content').hide();
                e.preventDefault();
                return false;
            });

            $(".accountLog").on('click', function(e) {
                //$('.accountLog').toggleClass('open');
            });

            //polling that gets the logs
            populateLogBox();
            setInterval(function() {populateLogBox()}, 5000);

            
            var im = document.getElementsByClassName('accountPicture')[0]; 
            im.onerror = function(){

                // image not found, change src as default image:
                im.src = 'http://www.dazzlepanel.com/projects/kurt/images/acc.png';
            };

            $('#uploadButton').click(function() {
                $('input[type=file]').trigger('click');
            });


            $('input[type=file]').change(function() {
                var file = $(this).val();
                $.get('/game/upload_user_pic', {'file': file}, function(data){
                    if(data == 1){                        
                        window.location.href = "/game/";
                        // maybe do some ajax to just reload the picture
                    }else{
                        alert("The picture you provided could not be used");
                    }
                });
            });
            
        });

        var canvasX = 800;
        var canvasY = 600;
        var fitX = 6;
        var fitY = 6;
        var halfFitX = Math.floor(fitX / 2);
        var halfFitY = Math.floor(fitY / 2);
        var sizeX = parseInt(canvasX / fitX);
        var sizeY = parseInt(canvasY / fitY);

        all_grass_levels=5
        var grass = [all_grass_levels];
        for	(index = 0; index < all_grass_levels; index++) {
            grass[index] = new Image();
            grass[index].src = "/static/images/forest/forest"+index+".png";
        }
        all_castle_levels=11
        var castle = [all_castle_levels];
        for	(index = 0; index < all_castle_levels; index++) {
            castle[index] = new Image();
            castle[index].src = "/static/images/castle/castle"+(index+1)+".png";
        }
        all_castle_levels=11
        var farm = [all_castle_levels];
        for	(index = 0; index < all_castle_levels; index++) {
            farm[index] = new Image();
            farm[index].src = "/static/images/farm/farm"+(index+1)+".png";
        }
        var house = [all_castle_levels];
        for	(index = 0; index < all_castle_levels; index++) {
            house[index] = new Image();
            house[index].src = "/static/images/house/house"+(index+1)+".png";
        }
        var lumbermill = [all_castle_levels];
        for	(index = 0; index < all_castle_levels; index++) {
            lumbermill[index] = new Image();
            lumbermill[index].src = "/static/images/lumbermill/lumbermill"+(index+1)+".png";
        }
        var stoneMine = [all_castle_levels];
        for	(index = 0; index < all_castle_levels; index++) {
            stoneMine[index] = new Image();
            stoneMine[index].src = "/static/images/stone_mine/stone_mine"+(index+1)+".png";
        }
        var goldMine = [all_castle_levels];
        for	(index = 0; index < all_castle_levels; index++) {
            goldMine[index] = new Image();
            goldMine[index].src = "/static/images/gold_mine/gold_mine"+(index+1)+".png";
        }

        var centreX = 5;
        var centreY = 5;
        var playerX = 0;
        var playerY = 0;
        var oldMouseXTile = -1;
        var oldMouseYTile = -1;

        var tileMap =""
        var rows = ""
        var tilesX = 0;
        var tilesY = 0;

        function setInitialPlayerLoc( x , y ){
            var tempX = x - halfFitX;
            var tempY = y - halfFitY;

            if (tempX < 0) {
                playerX = halfFitX;
            } else {
                if ( x + halfFitX > tilesX) {
                    playerX = tilesX - halfFitX;
                }else{
                    playerX = x;
                }
            }

            if (tempY < 0) {
                playerY = halfFitY;
            } else {
                if (y + halfFitY > tilesY) {
                    playerY = tilesY - halfFitY;
                }else{
                    playerY = y;
                }
            }
            centreX = playerX
            centreY = playerY
        }

        function getMap(){
            console.log("requesting map data");
            $.get('/game/get_map', function(data){
                console.log("received map data");
                tileMap = data;
                temp_rows = tileMap.split(';');
                tilesX = temp_rows[0].split(',').length;
                tilesY = temp_rows.length;
                rows = [tilesY];
                for(var i=0; i<tilesY; i++) {
                    rows[i] = new Array(tilesX);
                }
                for(var i=0;i<tilesY;i++){
                    row_contents = temp_rows[i].split(',');
                    for(var j=0;j<tilesX;j++){
                        rows[i][j]=row_contents[j];
                    }
                }
                initializeMapWithPlayerLoc();
            });
        }

        function initializeMapWithPlayerLoc(){
            $.get('/game/get_map_details', function(data){
                xy = data.split(',');
                setInitialPlayerLoc( parseInt(xy[0]) , parseInt(xy[1]) );
                resizeCanvas();

                $(window).off('resize');
                $(window).resize(function(e) {
                    resizeCanvas();
                });

                //window.addEventListener('resize', resizeCanvas, false);
            });
        }

        function moveRight() {
            //var fitX = canvasX/sizeX;
            //var halfFitX = fitX/2;
            var mapX = centreX - halfFitX;

            if (mapX < 0) {
                centreX += halfFitX;
            } else {
                if (centreX < (tilesX - halfFitX)) {
                    centreX += 1;
                }
            }
        }

        function moveLeft() {
            //var fitX = canvasX/sizeX;
            //var halfFitX = fitX/2;
            var mapX = centreX - halfFitX;

            if (mapX + fitX > tilesX) {
                centreX -= halfFitX;
            } else {
                if (centreX > halfFitX) {
                    centreX -= 1;
                }
            }
        }

        function moveUp() {
            //var fitY = canvasY/sizeY;
            //var halfFitY = fitY/2;
            var mapY = centreY - halfFitY;

            if (mapY + fitY > tilesY) {
                centreY -= halfFitY;
            } else {
                if (centreY > halfFitY) {
                    centreY -= 1;
                }
            }
        }

        function moveDown() {
            //var fitY = canvasY/sizeY;
            //var halfFitY = fitY/2;
            var mapY = centreY - halfFitY;

            if (mapY < 0) {
                centreY += halfFitY;
            } else {
                if (centreY < (tilesY - halfFitY)) {
                    centreY += 1;
                }
            }
        }
        /// expand with color, background etc.
        function drawTextBG(ctx, txt, x, y) {
            /// lets save current state as we make a lot of changes
            ctx.save();
            /// set font
            ctx.font = "Arial";
            /// draw text from top - makes life easier at the moment
            ctx.textBaseline = 'top';
            /// color for background
            ctx.fillStyle = '#468ccf';
            /// get width of text
            var width = ctx.measureText(txt).width;
            /// draw background rect assuming height of font
            ctx.fillRect(x, y, width, 15);
            /// text color
            ctx.fillStyle = '#000';
            /// draw text on top
            ctx.fillText(txt, x, y);
            /// restore original state
            ctx.restore();
        }

        function reDrawMap() {

            var canvas = document.getElementById('canvas');
            var context = canvas.getContext('2d');

            var mapX = centreX - halfFitX;
            var mapY = centreY - halfFitY;

            if (mapX < 0) {
                mapX = 0;
            } else if (mapX + fitX > tilesX) {
                mapX = tilesX - fitX;
            }
            if (mapY < 0) {
                mapY = 0;
            } else if (mapY + fitY > tilesY) {
                mapY = tilesY - fitY;
            }

            var mapX = Math.floor(mapX);
            var mapY = Math.floor(mapY);

            //draw positions
            var posX = 0;
            var posY = 0;

            context.font = "bold 15px Arial";
            context.fillStyle = "#ffb9af";
            // draw map
            for (var i = mapY; i < mapY + fitY; i++) {
                //console.log(rows[i]);
                endOfColumnCompensation=0
                if( i == mapY + fitY -1){
                    endOfColumnCompensation= canvas.height - (sizeY*fitY);
                    if(endOfColumnCompensation < 0){
                        endOfColumnCompensation=0;
                    }
                }
                for (var j = mapX; j < mapX + fitX; j++) {
                    endOfRowCompensation=0
                    if( j == mapX + fitX -1){
                        endOfRowCompensation= canvas.width - (sizeX*fitX);
                        if(endOfRowCompensation < 0){
                            endOfRowCompensation=0;
                        }
                    }
                    contents = rows[i][j];
                    contents = contents.split("-");
                    land_type = contents[0];
                    level = contents[2];
                    show_level = level -1;
                    context.drawImage(grass[0], posX, posY, sizeX+endOfRowCompensation, sizeY+endOfColumnCompensation);
                    switch (parseInt(land_type)) {
                        case 0:
                            r = Math.floor(Math.random()*all_grass_levels)
                            context.drawImage(grass[r], posX, posY, sizeX+endOfRowCompensation, sizeY+endOfColumnCompensation);
                            break;
                        case 1:
                            context.drawImage(house[show_level], posX, posY, sizeX+endOfRowCompensation, sizeY+endOfColumnCompensation);
                            break;
                        case 2:
                            context.drawImage(castle[show_level],0,0, castle[show_level].width/2 , castle[show_level].height/2 , posX, posY, sizeX+endOfRowCompensation, sizeY+endOfColumnCompensation);
                            break;
                        case 3:
                            context.drawImage(castle[show_level], castle[show_level].width/2 ,0, castle[show_level].width/2 , castle[show_level].height/2 , posX, posY, sizeX+endOfRowCompensation, sizeY+endOfColumnCompensation);
                            break;
                        case 4:
                            context.drawImage(farm[show_level], posX, posY, sizeX+endOfRowCompensation, sizeY+endOfColumnCompensation);
                            break;
                        case 5:
                            context.drawImage(castle[show_level],0,castle[show_level].height/2 , castle[show_level].width/2 , castle[show_level].height/2, posX, posY, sizeX+endOfRowCompensation, sizeY+endOfColumnCompensation);
                            break;
                        case 6:
                            context.drawImage(castle[show_level], castle[show_level].width/2 , castle[show_level].height/2 , castle[show_level].width/2 , castle[show_level].height/2 , posX, posY, sizeX+endOfRowCompensation, sizeY+endOfColumnCompensation);
                            break;
                        case 7:
                            context.drawImage(lumbermill[show_level], posX, posY, sizeX+endOfRowCompensation, sizeY+endOfColumnCompensation);
                            break;
                        case 8:
                            context.drawImage(stoneMine[show_level], posX, posY, sizeX+endOfRowCompensation, sizeY+endOfColumnCompensation);
                            break;
                        case 9:
                            context.drawImage(goldMine[show_level], posX, posY, sizeX+endOfRowCompensation, sizeY+endOfColumnCompensation);
                            break;
                        default:
                            break;
                    }
                    if(land_type != 0){
                    }
                    posX += sizeX;
                }
                posX = 0;
                posY += sizeY;
            }

            posX = 0;
            posY = 0;
            for (var i = mapY; i < mapY + fitY; i++) {
                for (var j = mapX; j < mapX + fitX; j++) {
                    contents = rows[i][j];
                    contents = contents.split("-");
                    land_type = contents[0];
                    username = contents[1];
                    level = contents[2];
                    if (land_type == "1"||land_type == "4"||land_type == "7"||land_type == "8"||land_type == "9") {
                        drawTextBG(context,level,posX+(sizeX*0.8), posY+(sizeY*0.8));
                    }
                    if (land_type == "5") {
                        drawTextBG(context,username,posX+(sizeX*0.8), posY+(sizeY*0.8));
                    }
                    posX += sizeX;
                }
                posX = 0;
                posY += sizeY;
            }
            context.font = "20px Arial";
            context.fillText("X:" + parseInt(centreX) + ", Y: " + parseInt(centreY), fitX*sizeX*0.81, fitY*sizeY*0.97);
        }

        window.onload = function () {

             $('[title!=""]').qtip();
            getMap();
            document.getElementById('canvas').style.cursor= 'url("http://www.arttime.ge/images/sc-graphics/openhand.png"), auto';
            document.getElementById('canvas').onmousedown = function () {
                document.getElementById('canvas').style.cursor= 'url("http://www.arttime.ge/images/sc-graphics/closedhand.png"), auto';
                this.style.position = 'relative';
                this.onmousemove = function (e) {
                    e = e || event;
                    this.onclick = null;
                    tileXPressed = parseInt(e.offsetX / sizeX);
                    tileYPressed = parseInt(e.offsetY / sizeY);
                    if (oldMouseXTile === -1) {
                        oldMouseXTile = tileXPressed;
                        oldMouseYTile = tileYPressed;
                    } else {
                        var modification = false;
                        if (oldMouseXTile !== tileXPressed) {
                            if (tileXPressed > oldMouseXTile) {
                                moveLeft();
                            } else {
                                moveRight();
                            }
                            modification = true;
                            oldMouseXTile = tileXPressed;
                        }
                        if (oldMouseYTile !== tileYPressed) {
                            if (tileYPressed > oldMouseYTile) {
                                moveUp();
                            } else {
                                moveDown();
                            }
                            modification = true;
                            oldMouseYTile = tileYPressed;
                        }
                        if (modification) {
                            reDrawMap();
                        }
                    }
                };

                this.onclick = function (e) {
                    e = e || event;
                    tileXPressed = parseInt(e.offsetX / sizeX);
                    tileYPressed = parseInt(e.offsetY / sizeY);
                    mapXPressed = tileXPressed - halfFitX + centreX;
                    mapYPressed = tileYPressed - halfFitY + centreY;
                    console.log("Clicked tile: " + tileXPressed + " , " + tileYPressed);
                    console.log("Clicked Map: " + mapXPressed + " , " + mapYPressed);

                    contents = rows[mapYPressed][mapXPressed];
                    contents = contents.split("-");
                    land_type = contents[0];
                    level = contents[1];

                    if(land_type == "5" || land_type == "6" || land_type == "2" || land_type == "3"){
                        console.log("clicked on " + level);
                        window.location.href = "/game/battle/"+level;
                    }
                };

                this.onmouseup = function () {
                    document.getElementById('canvas').style.cursor= 'url("http://www.arttime.ge/images/sc-graphics/openhand.png"), auto';
                    this.onmousemove = null;
                    oldMouseXTile = -1;
                    oldMouseYTile = -1;
                };

                document.onmouseup = function () {
                    document.getElementById('canvas').style.cursor= 'url("http://www.arttime.ge/images/sc-graphics/openhand.png"), auto';
                    document.getElementById('canvas').onmousemove = null;
                    oldMouseXTile = -1;
                    oldMouseYTile = -1;
                };
            };

            document.getElementById('canvas').ondragstart = function () {
                return false;
            };
        };

        function resizeCanvas() {

            //$("#table-supply").height($(document).height()-120-150);

            var canvas = document.getElementById('canvas');
            canvas.width = $("#canvas").parent().width();

            canvas.height = $("#table-supply").outerHeight();

            //canvas.height = $("#canvas").parent().height();
            canvasX = canvas.width;
            canvasY = canvas.height;
            sizeX = parseInt(canvasX / fitX);
            sizeY = parseInt(canvasY / fitY);
            reDrawMap();
        }
