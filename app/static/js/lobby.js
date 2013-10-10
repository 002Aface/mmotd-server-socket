/**
 * Lobby functions
 */

// compile handlebars templates ahead of time
var game_row_template_owned = Handlebars.compile($("#game-row-template-owned").html());
var game_row_template_unowned = Handlebars.compile($("#game-row-template-unowned").html());

// connect to socket in the /room namespace
var socket = io.connect('/lobby');

$(document).ready(function(){

    // attach a callback to chat input
    var new_game = document.getElementById('new-game');
    if (new_game.attachEvent) {
        new_game.attachEvent("click", newGame);
    } else {
        new_game.addEventListener("click", newGame);
    }

    loadGames();

    socket.on('connect', function() {
        console.log("socket connected");
        socket.emit('subscribe', {});
    });

    socket.on('disconnect', function() {
        console.log("socket disconnected");
    });

    socket.on('message', function(data) {
        console.log("Got message:", data);
    });

    socket.on('game_changed', function(data) {
        console.log("Got game_changed message:", data);
        loadGames();
    });

    socket.on('game_created', function(data) {
        console.log("Got game_created message:", data);
        loadGames();
    });

    socket.on('game_deleted', function(data) {
        console.log("Got game_deleted message:", data);
        loadGames();
    });

});


function loadGames(){
    $.ajax({
        url:"/api/games/",
        type:'GET',
        error:function(result){
            console.log(result);
        },
        success:function(result){
            $('#games-owned').html(game_row_template_owned(result))
            $('#games-unowned').html(game_row_template_unowned(result))
            $('.delete-button').click(function(evt){
                deleteGame(evt.target.id);
            });
        }
    });
}


function newGame(){
    $.ajax({
        url:"/api/games/",
        type:'POST',
        error:function(result){
            console.log('Unable to create game');
            console.log(result);
        },
        success:function(result){
            window.location.href = result.room_url;
        }
    });
}


// function that the admin can call to delete the game, which sends a message
// to all players, triggering a redirect back to the lobby
function deleteGame(game_id){
  $.ajax({
    url:"/api/games/" + game_id + "/delete/",
    type:'POST',
    error:function(result){
      console.log('Unable to delete game');
      console.log(result);
    },
    success:function(result){}
  });
}
