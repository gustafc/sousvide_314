var sv314 = function(window){
  function contentOf(selector) {
    return document.querySelector(selector).textContent
  }
  function showState(state) {
    function show(selector, show){
      document.querySelector(selector).style.display = show ? null : "none";
    }
    function formatTemp(t){
      return t.toFixed(2) + "\u00B0";
    }
    document.querySelector("#sv314_current_temp").innerHTML = formatTemp(state.current_temperature);
    document.querySelector("#sv314_target_temp").innerHTML = formatTemp(state.target_temperature);
    show("#sv314_is_heating", state.heating);
    show("#sv314_turn_on", !state.running);
    show("#sv314_turn_off", state.running);
    document.title = [].slice.call(document.querySelector("#sv314_temperature").childNodes).map(function(node){
      return (node.style && node.style.display === "none") ? "" : node.textContent;
    }).join("");
  }
  var syncStateRefreshes = promises.discardIfNotLatest();
  function refreshState(){
    syncStateRefreshes(ajax.get("/state")).then(JSON.parse).fin(function(){
      window.setTimeout(refreshState, api.updateInterval);
    }).done(showState);
  }
  function setRunning(isRunning, el){
    el.disabled = true;
    ajax.postJson("/state/running", isRunning).then(JSON.parse).fin(function(){
      el.disabled = false;
    }.bind(this)).done(showState);
  }
  function init(state){
    showState(state);
    window.setTimeout(refreshState, api.updateInterval);
    document.querySelector("#sv314_turn_on").addEventListener("click", setRunning.bind(null, true));
    document.querySelector("#sv314_turn_off").addEventListener("click", setRunning.bind(null, false));
    document.querySelector("#sv314_target_temp").addEventListener("click", function(){
      Q.fcall(function(){
        var suggested = parseFloat(contentOf("#sv314_target_temp"));
        return parseFloat(window.prompt("Enter new target temperature:", suggested));
      }).then(function(temp){
        return ajax.postJson("/state/target_temperature", temp).then(JSON.parse);
      }).done(showState);
    });
  }
  var api = {
    updateInterval: 1000,
    init: init
  };
  return api;
}(this);
