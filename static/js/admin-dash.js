(function() {
  var tap;

  tap = "click";

  if (Modernizr.touch) {
    tap = "touchstart";
  }

  $(document).on(tap, '.brick.closed', function(event) {
    var $this;
    $this = $(this);
    $this.animate({
      'width': '100%'
    }, 'fast', function() {});
    $this.removeClass('closed');
    return $this.addClass('open');
  });

  $(document).on(tap, '.brick a.js-close', function(event) {
    var $brick;
    $brick = $(this).closest('.brick');
    return $brick.animate({
      'width': '120px'
    }, 'fast', function() {
      $brick.removeClass('open');
      return $brick.addClass('closed');
    });
  });

}).call(this);