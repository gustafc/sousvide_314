var sv314 = function(window){
  function showState(state) {
    function show(selector, show){
      document.querySelector(selector).style.display = show ? null : "none";
    }
    function contentOf(selector) {
      return document.querySelector(selector).textContent
    }
    function formatTemp(t){
      return t.toFixed(2) + "\u00B0";
    }
    document.querySelector("#sv314_current_temp").innerHTML = formatTemp(state.current_temperature);
    document.querySelector("#sv314_target_temp").innerHTML = formatTemp(state.target_temperature);
    show("#sv314_is_heating", state.heating);
    show("#sv314_turn_on", !state.running);
    show("#sv314_turn_off", state.running);
    document.title = contentOf("#sv314_temperature");
  }
  var syncStateRefreshes = promises.discardIfNotLatest();
  function refreshState(){
    syncStateRefreshes(ajax.get("/state")).then(JSON.parse).fin(function(){
      window.setTimeout(refreshState, api.updateInterval);
    }).done(showState);
  }
  function init(state){
    showState(state);
    window.setTimeout(refreshState, api.updateInterval);
  }
  var api = {
    updateInterval: 1000,
    init: init
  };
  return api;
}(this);
