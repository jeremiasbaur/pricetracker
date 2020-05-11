var API = chrome || browser;
/**
 * CSS to hide everything on the page,
 * except for elements that have the "beastify-image" class.
 */
const hidePage = `body > :not(.beastify-image) {
                    display: none;
                  }`;

/**
 * Listen for clicks on the buttons, and send the appropriate message to
 * the content script in the page.
 */
function listenForClicks() {
	console.log("click");
  document.addEventListener("click", (e) => {
	/**
     * Given the name of a beast, get the URL to the corresponding image.
     */
    function beastNameToURL(beastName) {
      switch (beastName) {
        case "Frog":
          return API.extension.getURL("beasts/frog.jpg");
        case "Snake":
          return API.extension.getURL("beasts/snake.jpg");
        case "Turtle":
          return API.extension.getURL("beasts/turtle.jpg");
      }
    }

    /**
     * Insert the page-hiding CSS into the active tab,
     * then get the beast URL and
     * send a "beastify" message to the content script in the active tab.
     */
    function beastify(tabs) {
      API.tabs.insertCSS({code: hidePage}).then(() => {
        let url = beastNameToURL(e.target.textContent);
        API.tabs.sendMessage(tabs[0].id, {
          command: "beastify",
          beastURL: url
        });
      });
    }

    /**
     * Remove the page-hiding CSS from the active tab,
     * send a "reset" message to the content script in the active tab.
     */
    function reset(tabs) {
      API.tabs.removeCSS({code: hidePage}).then(() => {
        API.tabs.sendMessage(tabs[0].id, {
          command: "reset",
        });
      });
    }

    /**
     * Just log the error to the console.
     */
    function reportError(error) {
      console.error(`Could not beastify: ${error}`);
    }
	
	function getPrice(){
		var scripts = document.querySelectorAll('script[type="application/ld+json"]');

		var current_url = window.location.href;
		console.log(current_url)
		
		//let re = /(\d+)(?!.*\d)/;
		//var product_str = re.exec(current_url)[0];


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
		return price;
	}

    /**
     * Get the active tab,
     * then call "beastify()" or "reset()" as appropriate.
     */
    if (e.target.classList.contains("beast")) {
      API.tabs.query({active: true, currentWindow: true})
        .then(beastify)
        .catch(reportError);
    }
    else if (e.target.classList.contains("reset")) {
      API.tabs.query({active: true, currentWindow: true})
        .then(reset)
        .catch(reportError);
    }
	
	else if (e.target.classList.contains("price")) {
		document.querySelector("#price").text = "Price: " + getPrice();
    }
	
  });
}

/**
 * There was an error executing the script.
 * Display the popup's error message, and hide the normal UI.
 */
function reportExecuteScriptError(error) {
  document.querySelector("#popup-content").classList.add("hidden");
  document.querySelector("#error-content").classList.remove("hidden");
  console.error(`Failed to execute beastify content script: ${error.message}`);
}

/**
 * When the popup loads, inject a content script into the active tab,
 * and add a click handler.
 * If we couldn't inject the script, handle the error.
 */
API.tabs.executeScript({file: "/content_scripts/pricetracker.js"});
listenForClicks();
//.then(listenForClicks)
//.catch(reportExecuteScriptError);
