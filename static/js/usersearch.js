$(document).ready(function(){
            $('#searchButton').click(function(){
                window.location.href = "/game/user_search/"+document.getElementById("searchText").value;
            });
            $("#searchText").keyup(function(event){
                if(event.keyCode == 13){
                    $("#searchButton").click();
                }
            });
        });