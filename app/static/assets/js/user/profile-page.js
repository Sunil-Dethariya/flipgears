
const form = document.getElementById("profileForm");
const toast = document.getElementById("toast");
const inputs = document.querySelectorAll("input");
const editBtn = document.getElementById("editBtn");
const cancelBtn = document.getElementById("cancelBtn");
const saveBtn = document.getElementById("saveBtn");

editBtn.onclick = () => {
    inputs.forEach(i => i.disabled = false);
    saveBtn.style.display = "inline-block";
    cancelBtn.style.display = "inline";
    editBtn.style.display = "none";
};

cancelBtn.onclick = () => {
    inputs.forEach(i => i.disabled = true);
    saveBtn.style.display = "none";
    cancelBtn.style.display = "none";
    editBtn.style.display = "inline";
};

form.addEventListener("submit", function(e) {
    e.preventDefault(); // 🚫 stop page reload

    const formData = new FormData(form);

    fetch("", {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        },
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            inputs.forEach(i => i.disabled = true);
            saveBtn.style.display = "none";
            cancelBtn.style.display = "none";
            editBtn.style.display = "inline";

            toast.innerText = data.message;
            toast.classList.add("show");

            setTimeout(() => {
                toast.classList.remove("show");
            }, 3000);
        }
    });
});
