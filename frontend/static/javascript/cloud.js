var makeCloud = function(target, words) {
  var t = $(target);
  var width = Math.floor(t.width()/100)*100;
  var height = Math.floor(t.height()/100)*100;
  var oldWidth = t.attr("x-cloud-width");
  var oldHeight = t.attr("x-cloud-height");
  if(width != oldWidth || height != oldHeight) {
    t.attr("x-cloud-width", width);
    t.attr("x-cloud-height", height);
    d3.layout.cloud().size([width, height])
        .words(words)
        .rotate(function() { return 0; })
        .font("Open Sans")
        .fontSize(function(d) { return d.size; })
        .on("end", draw)
        .start();

    function draw(words) {
      t.empty();
      d3.select(target).append("svg").style("width", width).style("height", height)
        .append("g")
          .attr("transform", "translate(" + width/2 + "," + height/2 + ")")
        .selectAll("text")
          .data(words)
        .enter().append("a").attr("xlink:href", function(d) { return "/cloud/" + d.text } ).append("text")
          .style("font-size", function(d) { return d.size + "px"; })
          .attr("text-anchor", "middle")
          .attr("transform", function(d) {
            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
          })
          .text(function(d) { return d.text; });
    }
  }

  t.css("line-height", t.height() + "px");
}