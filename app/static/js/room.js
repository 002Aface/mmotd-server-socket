/**
** Chat/Waiting Room functions
**/

// compile handlebars templates ahead of time
var message_template = Handlebars.compile($("#message-template").html());
var players_template = Handlebars.compile($("#players-template").html());

// connect to socket in the /room namespace
var socket = io.connect('/room');

$(document).ready(function(){

    // attach a callback to chat input
    var form = document.getElementById('chat-form');
    if (form.attachEvent) {
        form.attachEvent("submit", processChatMessage);
    } else {
        form.addEventListener("submit", processChatMessage);
    }

    // attach a callback to start game button
    var delete_game = document.getElementById('delete-game');
    if (delete_game !== null) {
      if (delete_game.attachEvent) {
          delete_game.attachEvent("click", deleteGame);
      } else {
          delete_game.addEventListener("click", deleteGame);
      }
    }

    // attach a callback to leave game button
    var leave_game = document.getElementById('leave-game');
    if (leave_game !== null) {
      if (leave_game.attachEvent) {
          leave_game.attachEvent("click", leaveGame);
      } else {
          leave_game.addEventListener("click", leaveGame);
      }
    }

    // attach a callback to start game button
    var start_game = document.getElementById('start-game');
    if (start_game !== null) {
      if (start_game.attachEvent) {
          start_game.attachEvent("click", startGame);
      } else {
          start_game.addEventListener("click", startGame);
      }
    }

    socket.on('connect', function() {
        console.log("socket connected");
        socket.emit('subscribe', {game_id: game_id});
        updatePlayers();
    });

    socket.on('disconnect', function() {
        console.log("socket disconnected");
    });

    socket.on('message', function(data) {
        console.log("Got message:", data);
    });

    socket.on('chat', function(data) {
        console.log("Got chat message:", data);
        displayChatMessage(data);
    });

    socket.on('players_changed', function(data) {
        console.log("Got players_changed message:", data);
        updatePlayers();
    });

    socket.on('game_deleted', function(data) {
        console.log("Got game_deleted message:", data);
        leaveRoom();
    });

    socket.on('game_started', function(data) {
        console.log("Got game_started message:", data);
        joinGame();
    });

});

// function that adds a message to the chat
// pane when one is receieved over the socket
function displayChatMessage(message) {
  $('#chat-well').append(message_template(message));
  $('#chat-well').animate({ scrollTop: $('#chat-well').prop("scrollHeight") - $('#chat-well').height() }, 50);
}

// function that processes form input (from the chat
// box and pushes it down the socket to the other clients)
function processChatMessage(e) {

  // prevent default form action
  if (e.preventDefault) {
    e.preventDefault();
  }

  // send chat message to other connected clients
  socket.emit('chat', {game_id: game_id, message: $('#chat-input').val()});
  $('#chat-input').val('')
  // return false to prevent the default form behavior
  return false;

}


// function that makes an API call and updates the player list in the chat
// (eventually we'll have proper player_joined and player_left signals we can
// process directly from the socket, but this'll do for now)
function updatePlayers(){
    $.ajax({
        url:"/api/games/" + game_id + "/",
        type:'GET',
        error:function(result){
          console.log('Unable to retrieve game details');
          console.log(result);
        },
        success:function(result){
          $('#player-list').html(players_template(result));
        }
    });
}


// function that the admin can call to delete the game, which sends a message
// to all players, triggering a redirect back to the lobby
function deleteGame(){
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


// function that a player can call to leave the game, which sends a message to
// all players, triggering a redirect back to the lobby
function leaveGame(){
  $.ajax({
    url:"/api/games/" + game_id + "/leave/",
    type:'POST',
    error:function(result){
      console.log('Unable to leave game');
      console.log(result);
    },
    success:function(result){
      leaveRoom();
    }
  });
}


// function that the admin can call to start the game, which sends a message to
//all players, triggering a redirect directly into the game
function startGame(){
  $.ajax({
    url:"/api/games/" + game_id + "/start/",
    type:'POST',
    error:function(result){
      console.log('Unable to start game');
      console.log(result);
    },
    success:function(result){}
  });
}


// function that is called when the game starts, simply redirecting the user
// into the hangout
function joinGame(){
  window.location.href = "/game/" + game_id + '/';
}

// function that is called when the game is deleted or a player leaves the
// game, simply redirecting the user into the lobby
function leaveRoom(){
  window.location.href = "/lobby/";
}
