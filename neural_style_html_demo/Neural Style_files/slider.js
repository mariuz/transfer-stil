$(document).ready(function() {
  var changeImage = function() {
    $('.multi-style-shown').removeClass('multi-style-shown');
    $($('.multi-style-img')[$('#multi-style-slider').val()/10]).addClass('multi-style-shown');
  };
  var styleSlider = $('#multi-style-slider').bootstrapSlider({
      formatter: function(value) {
        return value + '% Van Gogh, ' + (100-value) + "% Picasso";
      }
  }).on('slide', changeImage);

  var changeImage2 = function() {
    $('.mp-shown').removeClass('mp-shown');
    console.log($('#mp-slider').val());
    $($('.mp-img')[$('#mp-slider').val()-1]).addClass('mp-shown');
  };
  var styleSlider = $('#mp-slider').bootstrapSlider({
    formatter: function(value) {
      if (value % 2 == 0) {
        return "alpha/beta value: 5e" + value/2;
      } else {
        return "alpha/beta value: 1e" + (value+1)/2;
      }
    }
  }).on('slide', changeImage2);
  var content_input_1_img = '<img src="2-content.jpg" style="width:200px"/>';
  $('#content-input-1').popover({ title: 'Picture of Stata', content: content_input_1_img, html:true});
  var style_input1_1_img = '<img src="2-style1.jpg" style="width:200px"/>';
  $('#style-input1-1').popover({ title: 'Picasso\'s \"Dora Maar\"', content: style_input1_1_img, html:true});
  var style_input2_1_img = '<img src="2-style2.jpg" style="width:200px"/>';
  $('#style-input2-1').popover({ title: 'Van Gogh\'s \"The Starry Night\"', content: style_input2_1_img, html:true});

  var ci2 = '<img src="marilyn.jpg" style="width:200px;"/>';
  $('#content-input-2').popover({ title: 'Picture of Marilyn Monroe', content: ci2, html:true});
  var si2 = '<img src="picasso2.jpg" style="width:200px"/>';
  $('#style-input-2').popover({ title: 'Picasso\'s \"The Dream\"', content: si2, html:true});

  var si3 = '<img src="munch-1.jpg" style="width:244px;"/>';
  $('#style-input-3').popover({ title: 'Munch\'s \"Self Portrait with Wine Bottle\"', content: si3, html:true});

});
