Slider = function (id_slider, id_select, values, trueValues ){
    var _id_slider = id_slider;
    var _id_select = id_select;
    var _values =  values;    
    var _trueValues = trueValues
                
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
    }
 }
