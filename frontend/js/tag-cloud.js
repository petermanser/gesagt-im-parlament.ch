function addTag($isotope_container, tag, weight) {
    var $text_element = $('<h2 style="font-size: '+ weight +'em;">' + tag + '</h2>')
    //console.log($text_element.css('width'))
            
    var $newItem = $('<div class="element" ></div>');
    $newItem.append($text_element);
    
    $isotope_container.isotope( 'insert', $newItem );
    $newItem.width($text_element.width() + 10);
    $newItem.height($text_element.height() + 10);
}