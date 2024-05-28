function addElementToHead(tagName, attributes) {
   // Erstelle das neue Element
   const newElement = document.createElement(tagName);

   // Setze die Attribute für das neue Element
   for (const key in attributes) {
      newElement.setAttribute(key, attributes[key]);
   }

   // Füge das neue Element zum <head> hinzu
   document.head.appendChild(newElement);
}

// Funktion zum Hinzufügen eines <noscript>-Elements zum <head>
function addNoScriptElement() {
   const noScriptElement = document.createElement("noscript");
   noScriptElement.innerHTML = `
      <div class="noscript alternative js-required">
         <p>
            This website requires JavaScript. Your browser doesn't
            support JavaScript or you have a JavaScript blocker
            installed.
         </p>
      </div>`;
   document.head.appendChild(noScriptElement);
}

// Beispiel: Mehrere Elemente hinzufügen
for (let i = 0; i < 3; i++) {
   addElementToHead("meta", {
      name: "keywords",
      content: "the sims 4, the sims, sims cc, sims mods"
   });

   addElementToHead("meta", {
      "http-equiv": "expires",
      content: "7"
   });

   addElementToHead("meta", {
      name: "revisit",
      content: "7 days"
   });

   addElementToHead("meta", {
      name: "audience",
      content: "all"
   });

   addElementToHead("meta", {
      name: "revisit-after",
      content: "7 days"
   });

   addElementToHead("meta", {
      name: "page-topic",
      content: "Sims"
   });

   addElementToHead("meta", {
      "http-equiv": "Content-Type",
      content: "text/html"
   });

   addElementToHead("link", {
      rel: "canonical",
      href: "https://simsinfohub.com"
   });

   addElementToHead("meta", {
      name: "author",
      content: "Jesper Mahel"
   });

   addElementToHead("meta", {
      name: "contact",
      content: "jesper@simsinfohub.com"
   });

   addElementToHead("meta", {
      name: "publisher",
      content: "Jesper Mahel"
   });

   addElementToHead("meta", {
      name: "copyright",
      content: "Jesper Mahel"
   });

   addNoScriptElement();

   addElementToHead("meta", {
      charset: "utf-8"
   });

   addElementToHead("meta", {
      name: "viewport",
      content: "width=device-width, initial-scale=1"
   });

   addElementToHead("link", {
      href: "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css",
      rel: "stylesheet",
      integrity:
         "sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH",
      crossorigin: "anonymous"
   });

   addElementToHead("link", {
      rel: "stylesheet",
      href: "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"
   });

   addElementToHead("script", {
      src: "/scripts/menufooter.js",
      async: ""
   });

   addElementToHead("script", {
      src: "/scripts/posthog.js",
      async: ""
   });

   addElementToHead("link", {
      href: "/static/css/styles.css",
      rel: "stylesheet"
   });

// addElementToHead("script", {
//    name: "defer",
//    "data-domain": "simsinfohub.com",
//    src: "https://plausible.io/js/script.js"
// });
}