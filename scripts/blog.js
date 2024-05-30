document.addEventListener("DOMContentLoaded", function () {
   // Function to fetch JSON data from a file
   function fetchJSONFile(path, callback) {
      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function () {
         if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
               var data = JSON.parse(xhr.responseText);
               if (callback) {
                  callback(data);
               }
            } else {
               console.error("Failed to fetch JSON data");
            }
         }
      };
      xhr.open("GET", path, true);
      xhr.send();
   }

   // Call the fetchJSONFile function to load data from the JSON file
   fetchJSONFile("/scripts/blogposts.json", function (jsonData) {
      // Sort data by published date (assuming the date is in a consistent format)
      jsonData.sort(function (a, b) {
         return new Date(b.published_date) - new Date(a.published_date);
      });

      // Get the card container
      var cardContainer = document.getElementById("cardContainer");

      // Loop through JSON data and generate HTML for each item
      jsonData.forEach(function (item) {
         // Replace placeholders in description with actual HTML anchor tags
         var description = item.description.replace(
            "[here]",
            '<a class="icon-link" href="' +
               item.link +
               '">here <i class="bi bi-box-arrow-up-right"></i></a>'
         );
         description = description.replace(
            "[Read more]",
            '<a class="icon-link" href="' +
               item.link +
               '">Read more <i class="bi bi-box-arrow-up-right"></i></a>'
         );
         description = description.replace(
            "[read more]",
            '<a class="icon-link" href="' +
               item.link +
               '">read more <i class="bi bi-box-arrow-up-right"></i></a>'
         );

         var cardHtml = `
            <div class="col">
                <div class="card h-100">
                    <div class="card-header">
                        ${item.type}
                    </div>
                    <img src="${item.image_src}" class="card-img-top" alt="${item.alt}" />
                    <div class="card-body">
                        <h5 class="card-title">${item.title}</h5>
                        <p class="card-text">${description}</p>
                        <!--<div class="d-grid gap-2"><a href="#" class="btn btn-primary">Go somewhere</a></div>-->
                    </div>
                    <div class="card-footer">
                        <small class="text-body-secondary">Published on ${item.published_date} by ${item.author}</small>
                    </div>
                </div>
            </div>
            `;
         cardContainer.innerHTML += cardHtml;
      });
   });
});