var promises = function(window){
  function discardIfNotLatest() {
    var serial = 0;
    return function(promise) {
      var thisSerial = ++serial;
      function endWith(fn) {
        return function(v){
          if (thisSerial === serial) {
            fn(v);
          }
        }
      }
      return Q.promise(function(resolve, reject){
        promise.done(endWith(resolve), endWith(reject));
      });
    };
  }
  return { discardIfNotLatest: discardIfNotLatest };
}(this);

var ajax = function(window) {
  function call(method, url, params) {
    return Q.promise(function(resolve, reject) {
      var req = new XMLHttpRequest();
      req.open(method, url);
      req.onload = function() {
        if (req.status == 200) {
          resolve(req.response);
        } else {
          reject(Error(req.statusText));
        }
      };
      req.onerror = reject.bind(null, Error("Network Error"));
      req.send(params);
    });
  }
  function get(url){
    return call("GET", url, null);
  }
  function postJson(url, data){
    return call("POST", url, JSON.stringify(data));
  }
  return { get: get, postJson: postJson };
}(this);
