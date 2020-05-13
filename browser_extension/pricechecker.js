function getPrice(){
	//document.body.style.border = "5px solid green";

	var scripts = document.querySelectorAll('script[type="application/ld+json"]');

	var current_url = window.location.href;

	//let re = /(\d+)(?!.*\d)/;
	let re = /(\d{7,8})(?!\d)/;
	var product_str = re.exec(current_url);

	if (product_str != null){
		product_str = product_str[0] || product_str;
		
		var price = null;
		var arrayLength = scripts.length;
		for (var i = 0; i < arrayLength; i++) {
			var json = JSON.parse(scripts[i].text);
			
			if (json.sku != null && current_url.includes(json.sku)){
				price = Math.min(json.offers.highPrice, json.offers.lowPrice);
				break;
			}
		}

		if (price != null){
			console.log("success");
			console.log(price);
		} else{
			console.log("failed");
		}
	}
	else {
		console.log("currently not on product page");
		
	}
	
	browser.runtime.sendMessage({price: price, product_id: product_str});
}

browser.runtime.onMessage.addListener((message) => {
    if (message.command === "getPrice") {
      getPrice();
    }
});