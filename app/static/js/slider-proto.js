function Slider(id_slider, id_select){
    this.id_slider = id_slider;
    this.id_select = id_select;
    
    this.trueValues = [604800, 1209600,1814400, /*weeks: 1 to 3*/
        2419200,4838400,7257600,9676800,12096000,14515200,16934400,19353600,21772800,24192000,26611200, /*months: 1 to 11*/
        29030400, 58060800, 87091200]; /*years: 1 to 3*/ /*17 items*/
        
    this.values =  [0,3,6, /*scale in diferent proportion*/
                9,14,19,24,29,34,39,44,49,54,59,
                76,88,100];
    
    this.put_slider = function(){
        this.createSlider();
        this.changeSelect();
    }
 }
 
Slider.prototype.findNearest = function (includeLeft, includeRight, value) {
    var nearest = null;
    var diff = null;
    for (var i = 0; i < _values.length; i++) {
        if ((includeLeft && this.values[i] <= value) || (includeRight && this.values[i] >= value)) {
            var newDiff = Math.abs(value - this.values[i]);
            if (diff == null || newDiff < diff) {
                    nearest = this.values[i];
                    diff = newDiff;
            }
        }
    }
    return nearest;
}

Slider.prototype.getRealValue = function (value, values1, values2) {
    for (var i = 0; i < values1.length; i++) {
        if (values1[i] >= value) {
            return values2[i];
        }
    }
    return 0;
}

Slider.prototype.valueSelected = function (){
    $(this.id_select+" option:selected").each(function () {
            val = $(this).val();
    });
    return val
}


Slider.prototype.changeSelect = function(){
    $(this.id_select).change(function () {
        this.changeSlider();
    })
}

Slider.prototype.changeSlider = function (){
    val = valueSelected(this.id_select)
    $(this.id_slider).slider('option','value',this.getRealValue(val,this.trueValues,this.values))
}

Slider.prototype.createSlider = function(){
    var slider = $(this.id_slider).slider({
        min: 0,
        max: 100,
        value: this.getRealValue(valueSelected(),this.trueValues,this.values),
        slide: function(event, ui) {
                var includeLeft = event.keyCode != $.ui.keyCode.RIGHT;
                var includeRight = event.keyCode != $.ui.keyCode.LEFT;
                slider.slider('option', 'value', this.findNearest(includeLeft, includeRight, ui.value));
                $(this.id_select).val(this.getRealValue(slider.slider('value'),this.values,this.trueValues))
                return false;
        }
    });
}