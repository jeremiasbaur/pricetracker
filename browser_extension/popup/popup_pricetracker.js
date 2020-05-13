//var browser = chrome || browser;
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
  document.addEventListener("click", (e) => {
	/**
     * Given the name of a beast, get the URL to the corresponding image.
     */
    function beastNameToURL(beastName) {
      switch (beastName) {
        case "Frog":
          return browser.extension.getURL("beasts/frog.jpg");
        case "Snake":
          return browser.extension.getURL("beasts/snake.jpg");
        case "Turtle":
          return browser.extension.getURL("beasts/turtle.jpg");
      }
    }

    /**
     * Insert the page-hiding CSS into the active tab,
     * then get the beast URL and
     * send a "beastify" message to the content script in the active tab.
     */
    function beastify(tabs) {
      browser.tabs.insertCSS({code: hidePage}).then(() => {
        let url = beastNameToURL(e.target.textContent);
        browser.tabs.sendMessage(tabs[0].id, {
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
      browser.tabs.removeCSS({code: hidePage}).then(() => {
        browser.tabs.sendMessage(tabs[0].id, {
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
	
	function getPrice(tabs){
		browser.tabs.sendMessage(tabs[0].id, {
          command: "getPrice"
        });
	}

    /**
     * Get the active tab,
     * then call "beastify()" or "reset()" as appropriate.
     */
    if (e.target.classList.contains("beast")) {
      browser.tabs.query({active: true, currentWindow: true})
        .then(beastify)
        .catch(reportError);
    }
    else if (e.target.classList.contains("reset")) {
      browser.tabs.query({active: true, currentWindow: true})
        .then(reset)
        .catch(reportError);
    }
	
	else if (e.target.classList.contains("price")) {
		browser.tabs.query({active: true, currentWindow: true})
        .then(getPrice);
		
    } else if(e.target.href!==undefined){
		chrome.tabs.create({url:e.target.href})
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
browser.tabs.executeScript({file: "../browser-polyfill.js"});
browser.tabs.executeScript({file: "/content_scripts/pricetracker.js"})
.then(listenForClicks)
.catch(reportExecuteScriptError);

function setPrice(price_info){
	console.log("here");
	document.querySelector("#price").innerHTML = "Price: " + price_info.price;
	document.querySelector("#product_id").innerHTML = "Product ID: " + price_info.product_id;
	
	var response;
	getPriceAPI('digitec', price_info.product_id, 0).then(data => {
		document.querySelector("#top_price").innerHTML = "Top Price: " + data.top_price;
		document.querySelector("#top_price_shop").innerHTML = "Top Shop: " + data.shop;
		
		document.querySelector("#topurl").setAttribute('href', data.url);
	});	
}

async function getPriceAPI(shop, product_id, type) 
{	
	console.log(`http://localhost:5000/api/v1/prices/${shop}/${product_id}/${type}`);
  let response = await fetch(`http://localhost:5000/api/v1/prices/${shop}/${product_id}/${type}`);
  let data = await response.json()
  return data;
}

// communication from content script

function handleMessage(request){
	if (request.price){
		setPrice({price: request.price, product_id: request.product_id});
	}
	console.log(request);
}

browser.runtime.onMessage.addListener(handleMessage);