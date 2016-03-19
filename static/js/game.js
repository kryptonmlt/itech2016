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

            collectTimer();
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
                                $('#farms_gold_cost').html(res[2]);
                                $('#farms_lumber_cost').html(res[3]);
                                $('#farms_stone_cost').html(res[4]);
                                break;
                           case "wall":
                                console.log(data);
                                var res = data.split(",");
                                $('#wallLevel').html(res[0]);
                                $('#walls_gold_cost').html(res[1]);
                                $('#walls_lumber_cost').html(res[2]);
                                $('#walls_stone_cost').html(res[3]);
                                break;
                           case "stone_caves":
                                var res = data.split(",");
                                $('#stone_caves').html(res[0]);
                                $('#stone_mine_gold_cost').html(res[1]);
                                $('#stone_mine_lumber_cost').html(res[2]);
                                $('#stone_mine_stone_cost').html(res[3]);
                                break;
                           case "gold_mines":
                                var res = data.split(",");
                                $('#gold_mines').html(res[0]);
                                $('#gold_mine_gold_cost').html(res[1]);
                                $('#gold_mine_lumber_cost').html(res[2]);
                                $('#gold_mine_stone_cost').html(res[3]);
                                break;
                           case "lumber_mills":
                                var res = data.split(",");
                                $('#lumber_mills').html(res[0]);
                                $('#lumber_mill_gold_cost').html(res[1]);
                                $('#lumber_mill_lumber_cost').html(res[2]);
                                $('#lumber_mill_stone_cost').html(res[3]);
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
        });

        var canvasX = 800;
        var canvasY = 600;
        var fitX = 9;
        var fitY = 9;
        var halfFitX = Math.floor(fitX / 2);
        var halfFitY = Math.floor(fitY / 2);
        var sizeX = parseInt(canvasX / fitX);
        var sizeY = parseInt(canvasY / fitY);

        var grass = new Image();
        var castle = new Image();
        var farm = new Image();
        var lumbermill = new Image();
        var stoneMine = new Image();
        var goldMine = new Image();
        var house = new Image();
        grass.src = "http://kurtportelli.com/kurtftp/resources/forest1.jpg";
        castle.src = "http://kurtportelli.com/kurtftp/resources/castle1_merged.png";
        farm.src = "http://kurtportelli.com/kurtftp/resources/farm_merged.png";
        lumbermill.src = "http://kurtportelli.com/kurtftp/resources/lumbermill_merged.png";
        stoneMine.src = "http://kurtportelli.com/kurtftp/resources/stone_mine_merged.png";
        goldMine.src = "http://kurtportelli.com/kurtftp/resources/gold_mine_merged.png";
        house.src = "http://kurtportelli.com/kurtftp/resources/house_merged.png";

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
                $.get('/game/get_map_details', function(data){
                    xy = data.split(',');
                    setInitialPlayerLoc( parseInt(xy[0]) , parseInt(xy[1]) );
                    resizeCanvas();
                });
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
                for (var j = mapX; j < mapX + fitX; j++) {
                    contents = rows[i][j];
                    contents = contents.split("-");
                    land_type = contents[0];
                    level = contents[1];
                    switch (parseInt(land_type)) {
                        case 0:
                            context.drawImage(grass, posX, posY, sizeX, sizeY);
                            break;
                        case 1:
                            context.drawImage(house, posX, posY, sizeX, sizeY);
                            break;
                        case 2:
                            context.drawImage(castle, posX, posY, sizeX, sizeY);
                            break;
                        case 3:
                            context.drawImage(castle, posX, posY, sizeX, sizeY);
                            break;
                        case 4:
                            context.drawImage(farm, posX, posY, sizeX, sizeY);
                            break;
                        case 5:
                            context.drawImage(castle, posX, posY, sizeX, sizeY);
                            break;
                        case 6:
                            context.drawImage(castle, posX, posY, sizeX, sizeY);
                            break;
                        case 7:
                            context.drawImage(lumbermill, posX, posY, sizeX, sizeY);
                            break;
                        case 8:
                            context.drawImage(stoneMine, posX, posY, sizeX, sizeY);
                            break;
                        case 9:
                            context.drawImage(goldMine, posX, posY, sizeX, sizeY);
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
                    level = contents[1];
                    if (land_type == "1"||land_type == "4"||land_type == "7"||land_type == "8"||land_type == "9") {
                        drawTextBG(context,level,posX+(sizeX*0.8), posY+(sizeY*0.8));
                    }
                    if (land_type == "5") {
                        drawTextBG(context,level,posX+(sizeX*0.8), posY+(sizeY*0.8));
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
                };

                this.onmouseup = function () {
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

        window.addEventListener('resize', resizeCanvas, false);

        function resizeCanvas() {

            var canvas = document.getElementById('canvas');
            canvas.width = $("#canvas").parent().width();
            canvas.height = $("#canvas").parent().height();
            canvasX = canvas.width;
            canvasY = canvas.height;
            sizeX = parseInt(canvasX / fitX);
            sizeY = parseInt(canvasY / fitY);
            reDrawMap();
        }