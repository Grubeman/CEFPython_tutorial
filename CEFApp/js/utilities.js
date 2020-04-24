console.log("utilities are loaded")

var set_inner_html = function(css_selector, innerhtml) {
    console.log("setting "+css_selector+" innerhtml")
    if ($(css_selector).length == 1) {
        $(css_selector).html(innerhtml)
    }
    else {
        console.log("Incorrect css_selector :"+css_selector)
    }
}

var console_log = function(msg) {
    console.log(msg)
}