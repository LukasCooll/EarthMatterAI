document.getElementById("uploadForm").addEventListener("submit", async function(e){
    e.preventDefault();

    const fileInput = document.getElementById("file");
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("image", file);

    const response = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    console.log(data);
});