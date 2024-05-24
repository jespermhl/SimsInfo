function loadMenu() {
   fetch("/components/menu.html")
      .then((response) => response.text())
      .then((data) => {
         document.getElementById("menu").innerHTML = data;
         addActiveClassToNavLinks();
      });
}

function loadFooter() {
   fetch("/components/footer.html")
      .then((response) => response.text())
      .then((data) => {
         document.getElementById("footer").innerHTML = data;
      });
}

function addActiveClassToNavLinks() {
   var currentUrl = window.location.href;
   console.log(currentUrl);
   currentUrl = currentUrl.replace("localhost", "");
   console.log(currentUrl);
   currentUrl = currentUrl.replace("simsinfo.2ix.de", "");
   console.log(currentUrl);
   currentUrl = currentUrl.replace("https://", "");
   console.log(currentUrl);
   currentUrl = currentUrl.replace("http://", "");
   console.log(currentUrl);
   currentUrl = currentUrl.replace(":8000", "");
   console.log(currentUrl);
   currentUrl = currentUrl.replace("index.html", "");
   console.log(currentUrl);
   currentUrl = currentUrl.replace("simsinfo.netlify.app", "");
   console.log(currentUrl);
   currentUrl = currentUrl.replace("simsinfohub.com", "");
   console.log(currentUrl);

   fetch("/scripts/menulinks.json")
      .then((response) => response.json())
      .then((data) => {
         var navLinks = data;
         console.log(navLinks); // Zeigt die geladenen Daten in der Konsole an

         for (var i = 0; i < navLinks.length; i++) {
            var link = navLinks[i];
            var navElement = document.getElementById(link.id);

            if (navElement) {
               if (currentUrl.includes(link.url)) {
                  navElement.classList.add("active");
                  navElement.setAttribute("aria-current", "page");
               } else {
                  navElement.classList.remove("active");
                  navElement.removeAttribute("aria-current");
               }
            } else {
               console.error(
                  "Element mit der ID '" + link.id + "' nicht gefunden."
               );
            }
         }
      })
      .catch((error) =>
         console.error("Fehler beim Laden der JSON-Daten:", error)
      );
}

window.onload = function () {
   loadMenu();
   loadFooter();
};