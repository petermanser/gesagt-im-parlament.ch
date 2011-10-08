function addTagMap($isotope_container, tag_map) {
    var min = 0,
        max = 0,
        diff = 0,
        fct = 0;
        
    for (var tag in tag_map) { // find range of values
        var value = tag_map[tag][0];
        if (value < min) min = value;
        if (value > max) max = value;
    }
    diff = max - min;
    fct = 6 / diff; // we want values between 1 and 6
    
    for (var tag in tag_map) {
        addTag($isotope_container, tag, tag_map[tag][0] * fct, tag_map[tag][1]);
    }
}

function addTag($isotope_container, tag, weight, sentiment) {
	  var $color = 'black'
	  
     if ( sentiment < -(6 + weight/3) ) {
        $color = 'red';
      }
	
     if ( sentiment > (6 + weight/3) ) {
        $color = 'green';
      }
	
      var $text_element = $('<h2 style="font-size: '+ weight +'em; color: '+ $color +'">' + tag + '</h2>')
      //console.log($text_element.css('width'))

      var $newItem = $('<div id="$'+ tag +'" class="element" ></div>');
      $newItem.append($text_element);

      $isotope_container.isotope( 'insert', $newItem );
      $newItem.width($text_element.width() + 10);
      $newItem.height($text_element.height() + 10);
}
 
function removeAllTags($isotope_container) {
    tagSet = $isotope_container.find('.element');
    for (i=0; i<tagSet.length; i++) {
        var $tag = $(tagSet[i]);
        $isotope_container.isotope( 'remove', $tag )   
    }
    
}