Slider = function (id_slider, id_select){
    _id_slider = id_slider;
    _id_select = id_select;
    number = 0;
    _trueValues = [604800, 1209600,1814400, /*weeks: 1 to 3*/
        2419200,4838400,7257600,9676800,12096000,14515200,16934400,19353600,21772800,24192000,26611200, /*months: 1 to 11*/
        29030400, 58060800, 87091200]; /*years: 1 to 3*/ /*17 items*/
        
    _values =  [0,3,6, /*scale in diferent proportion*/
                9,14,19,24,29,34,39,44,49,54,59,
                76,88,100];
                
    var findNearest = function (includeLeft, includeRight, value) {
        var nearest = null;
        var diff = null;
        for (var i = 0; i < _values.length; i++) {
            if ((includeLeft && _values[i] <= value) || (includeRight && _values[i] >= value)) {
                var newDiff = Math.abs(value - _values[i]);
                if (diff == null || newDiff < diff) {
                    nearest = _values[i];
                    diff = newDiff;
                }
            }
        }
        return nearest;
    }
    
    var getRealValue = function (value, values1, values2) {
        for (var i = 0; i < values1.length; i++) {
            if (values1[i] >= value) {
                return values2[i];
            }
        }
        return 0;
    }

    var changeSlider = function (){
        val = valueSelected(_id_select);
        $(_id_slider).slider('option','value',getRealValue(val,_trueValues,_values));
    }

    var changeSelect = function(){
        $(_id_select).change(function () {
            changeSlider();
        })
    }

    var valueSelected = function (){
        $(_id_select+" option:selected").each(function () {
                val = $(this).val();
        });
        return val;
    }
    
    this.put_slider = function(){
        var slider = $(_id_slider).slider({
            min: 0,
            max: 100,
            value: getRealValue(valueSelected(),_trueValues,_values),
            slide: function(event, ui) {
                    var includeLeft = event.keyCode != $.ui.keyCode.RIGHT;
                    var includeRight = event.keyCode != $.ui.keyCode.LEFT;
                    slider.slider('option', 'value', findNearest(includeLeft, includeRight, ui.value));
                    $(_id_select).val(getRealValue(slider.slider('value'),_values,_trueValues));
                    return false;
            }
        });
        changeSelect();
        number++;
    }
 }
